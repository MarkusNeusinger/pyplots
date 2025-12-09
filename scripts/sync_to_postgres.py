#!/usr/bin/env python3
"""
Sync plots from repository to PostgreSQL.

This script is run by GitHub Actions on push to main branch.
It ensures the database only contains data for code that is actually in main.

New structure (plots/{spec_id}/):
- spec.md: Spec description, data requirements, use cases
- metadata.yaml: Tags, implementation metadata, generation history
- implementations/{library}.py: Library-specific implementation code
"""

import asyncio
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv


load_dotenv()

from sqlalchemy import delete, select  # noqa: E402
from sqlalchemy.dialects.postgresql import insert  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from core.database import LIBRARIES_SEED, Implementation, Library, Spec  # noqa: E402


# Configuration
BASE_DIR = Path(__file__).parent.parent
PLOTS_DIR = BASE_DIR / "plots"
GCS_BUCKET = os.getenv("GCS_BUCKET", "pyplots-images")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def parse_spec_markdown(file_path: Path) -> dict:
    """
    Parse a spec.md file and extract metadata.

    Args:
        file_path: Path to the spec.md file

    Returns:
        Dict with title, description, content, data_requirements, tags
    """
    content = file_path.read_text(encoding="utf-8")
    spec_id = file_path.parent.name  # Directory name is spec_id

    # Parse title from first heading: "# scatter-basic: Basic Scatter Plot"
    title_match = re.search(r"^#\s+[\w-]+:\s*(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else spec_id

    # Parse description section
    description = ""
    desc_match = re.search(r"## Description\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()

    # Parse data requirements section
    data_requirements = []
    data_match = re.search(r"## Data\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if data_match:
        data_section = data_match.group(1)
        for match in re.finditer(r"-\s+`(\w+)`\s+\((\w+)\)\s*-?\s*(.+)?", data_section):
            data_requirements.append(
                {"name": match.group(1), "type": match.group(2), "description": (match.group(3) or "").strip()}
            )

    # Parse simple tags from Tags section (if present)
    tags = []
    tags_match = re.search(r"## Tags\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if tags_match:
        tags_text = tags_match.group(1).strip()
        tags = [t.strip() for t in tags_text.split(",") if t.strip()]

    return {
        "id": spec_id,
        "title": title,
        "description": description,
        "content": content,  # Store full markdown
        "data_requirements": data_requirements,
        "tags": tags,
    }


def parse_metadata_yaml(file_path: Path) -> dict | None:
    """
    Parse a metadata.yaml file.

    Args:
        file_path: Path to the metadata.yaml file

    Returns:
        Dict with spec_id, title, tags, implementations or None if invalid
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if not data or "spec_id" not in data:
            return None
        return data
    except Exception as e:
        logger.error(f"Failed to parse metadata {file_path}: {e}")
        return None


def scan_plot_directory(plot_dir: Path) -> dict | None:
    """
    Scan a single plot directory and extract all data.

    Args:
        plot_dir: Path to the plot directory (e.g., plots/scatter-basic/)

    Returns:
        Dict with spec data, metadata, and implementations
    """
    spec_id = plot_dir.name
    spec_file = plot_dir / "spec.md"
    metadata_file = plot_dir / "metadata.yaml"
    implementations_dir = plot_dir / "implementations"

    if not spec_file.exists():
        logger.warning(f"No spec.md found in {plot_dir}")
        return None

    # Parse spec
    spec_data = parse_spec_markdown(spec_file)

    # Parse metadata (optional)
    metadata = {}
    if metadata_file.exists():
        metadata = parse_metadata_yaml(metadata_file) or {}

    # Merge title from metadata if available
    if metadata.get("title"):
        spec_data["title"] = metadata["title"]

    # Add structured tags from metadata
    spec_data["structured_tags"] = metadata.get("tags")

    # Scan implementations
    implementations = []
    if implementations_dir.exists():
        for impl_file in implementations_dir.glob("*.py"):
            if impl_file.name.startswith("_"):
                continue

            library_id = impl_file.stem  # e.g., "matplotlib", "seaborn"
            code = impl_file.read_text(encoding="utf-8")
            file_path = str(impl_file.relative_to(BASE_DIR))

            # Get implementation metadata
            impl_meta = metadata.get("implementations", {}).get(library_id, {})
            current = impl_meta.get("current") or {}

            # Parse generated_at
            generated_at = current.get("generated_at")
            if isinstance(generated_at, str):
                try:
                    generated_at = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
                except ValueError:
                    generated_at = None

            implementations.append({
                "spec_id": spec_id,
                "library_id": library_id,
                "variant": "default",
                "file_path": file_path,
                "code": code,
                "preview_url": impl_meta.get("preview_url") or get_gcs_preview_url(spec_id, library_id),
                "generated_at": generated_at,
                "generated_by": current.get("generated_by"),
                "workflow_run": current.get("workflow_run"),
                "issue_number": current.get("issue"),
                "quality_score": current.get("quality_score"),
            })

    return {
        "spec": spec_data,
        "implementations": implementations,
    }


def get_gcs_preview_url(spec_id: str, library: str, variant: str = "default") -> str:
    """
    Get the GCS preview URL for an implementation.

    Args:
        spec_id: The specification ID
        library: The library name
        variant: The variant name (default: "default")

    Returns:
        Public GCS URL
    """
    return f"https://storage.googleapis.com/{GCS_BUCKET}/plots/{spec_id}/{library}/{variant}/"


async def sync_to_database(session: AsyncSession, plots: list[dict]) -> dict:
    """
    Sync plots to the database.

    Args:
        session: Database session
        plots: List of plot data dictionaries

    Returns:
        Dict with counts of synced/removed items
    """
    stats = {"specs_synced": 0, "specs_removed": 0, "impls_synced": 0, "impls_removed": 0}

    # Ensure libraries exist
    for lib_data in LIBRARIES_SEED:
        stmt = insert(Library).values(**lib_data).on_conflict_do_nothing(index_elements=["id"])
        await session.execute(stmt)

    # Collect all spec IDs and implementation keys
    spec_ids = set()
    impl_keys = set()

    for plot_data in plots:
        spec = plot_data["spec"]
        spec_id = spec["id"]
        spec_ids.add(spec_id)

        # Upsert spec
        stmt = (
            insert(Spec)
            .values(**spec)
            .on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "title": spec["title"],
                    "description": spec["description"],
                    "content": spec["content"],
                    "data_requirements": spec["data_requirements"],
                    "tags": spec["tags"],
                    "structured_tags": spec.get("structured_tags"),
                },
            )
        )
        await session.execute(stmt)
        stats["specs_synced"] += 1

        # Upsert implementations
        for impl in plot_data["implementations"]:
            key = (impl["spec_id"], impl["library_id"], impl["variant"])
            impl_keys.add(key)

            update_set = {
                "file_path": impl["file_path"],
                "code": impl["code"],
                "preview_url": impl["preview_url"],
            }

            # Add optional fields
            for field in ["generated_at", "generated_by", "workflow_run", "issue_number", "quality_score"]:
                if impl.get(field) is not None:
                    update_set[field] = impl[field]

            stmt = (
                insert(Implementation)
                .values(**impl)
                .on_conflict_do_update(constraint="uq_implementation", set_=update_set)
            )
            await session.execute(stmt)
            stats["impls_synced"] += 1

    # Remove specs that no longer exist in repo
    result = await session.execute(select(Spec.id).where(Spec.id.notin_(spec_ids)))
    removed_spec_ids = [row[0] for row in result.fetchall()]
    if removed_spec_ids:
        await session.execute(delete(Spec).where(Spec.id.in_(removed_spec_ids)))
        stats["specs_removed"] = len(removed_spec_ids)
        logger.info(f"Removed {len(removed_spec_ids)} specs no longer in repo")

    # Remove implementations that no longer exist in repo
    result = await session.execute(select(Implementation.spec_id, Implementation.library_id, Implementation.variant))
    existing_impls = [(row[0], row[1], row[2]) for row in result.fetchall()]

    removed_impls = [impl for impl in existing_impls if impl not in impl_keys]
    if removed_impls:
        for spec_id, library_id, variant in removed_impls:
            await session.execute(
                delete(Implementation).where(
                    Implementation.spec_id == spec_id,
                    Implementation.library_id == library_id,
                    Implementation.variant == variant,
                )
            )
        stats["impls_removed"] = len(removed_impls)
        logger.info(f"Removed {len(removed_impls)} implementations no longer in repo")

    await session.commit()
    return stats


async def main() -> int:
    """Main entry point for the sync script."""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not set")
        return 1

    logger.info("Starting sync to PostgreSQL...")
    logger.info(f"Plots directory: {PLOTS_DIR}")

    # Scan all plot directories
    plots = []
    if PLOTS_DIR.exists():
        for plot_dir in sorted(PLOTS_DIR.iterdir()):
            if not plot_dir.is_dir():
                continue
            if plot_dir.name.startswith("."):
                continue

            plot_data = scan_plot_directory(plot_dir)
            if plot_data:
                plots.append(plot_data)
                logger.debug(f"Scanned plot: {plot_dir.name}")

    logger.info(f"Found {len(plots)} plots")

    total_impls = sum(len(p["implementations"]) for p in plots)
    logger.info(f"Found {total_impls} implementations")

    # Create database connection
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with async_session() as session:
            stats = await sync_to_database(session, plots)

        logger.info("Sync completed successfully!")
        logger.info(f"  Specs synced: {stats['specs_synced']}, removed: {stats['specs_removed']}")
        logger.info(f"  Implementations synced: {stats['impls_synced']}, removed: {stats['impls_removed']}")
        return 0

    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return 1

    finally:
        await engine.dispose()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
