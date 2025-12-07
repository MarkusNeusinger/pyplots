#!/usr/bin/env python3
"""
Sync specs and implementations from repository to PostgreSQL.

This script is run by GitHub Actions on push to main branch.
It ensures the database only contains data for code that is actually in main.
"""

import asyncio
import logging
import os
import re
import sys
from pathlib import Path


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
SPECS_DIR = BASE_DIR / "specs"
PLOTS_DIR = BASE_DIR / "plots"
GCS_BUCKET = os.getenv("GCS_BUCKET", "pyplots-images")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def parse_spec_markdown(file_path: Path) -> dict:
    """
    Parse a spec markdown file and extract metadata.

    Args:
        file_path: Path to the .md file

    Returns:
        Dict with id, title, description, data_requirements, tags
    """
    content = file_path.read_text(encoding="utf-8")
    spec_id = file_path.stem

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
        # Extract required columns: - `x` (numeric) - description
        for match in re.finditer(r"-\s+`(\w+)`\s+\((\w+)\)\s*-?\s*(.+)?", data_section):
            data_requirements.append({
                "name": match.group(1),
                "type": match.group(2),
                "description": (match.group(3) or "").strip(),
            })

    # Parse tags section
    tags = []
    tags_match = re.search(r"## Tags\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if tags_match:
        tags_text = tags_match.group(1).strip()
        tags = [t.strip() for t in tags_text.split(",") if t.strip()]

    return {
        "id": spec_id,
        "title": title,
        "description": description,
        "data_requirements": data_requirements,
        "tags": tags,
    }


def scan_implementations() -> list[dict]:
    """
    Scan the plots directory for all implementations.

    Returns:
        List of dicts with spec_id, library_id, plot_function, variant, file_path
    """
    implementations = []
    excluded_specs = {".template", "VERSIONING"}

    if not PLOTS_DIR.exists():
        logger.warning(f"Plots directory not found: {PLOTS_DIR}")
        return implementations

    # Pattern: plots/{library}/{plot_function}/{spec_id}/{variant}.py
    for py_file in PLOTS_DIR.rglob("*.py"):
        # Skip __pycache__ and other non-implementation files
        if "__pycache__" in str(py_file) or py_file.name.startswith("_"):
            continue

        parts = py_file.relative_to(PLOTS_DIR).parts
        if len(parts) >= 4:
            library = parts[0]
            plot_function = parts[1]
            spec_id = parts[2]
            variant = py_file.stem  # "default" or "ggplot_style"

            if spec_id in excluded_specs:
                continue

            # Verify the spec exists
            spec_file = SPECS_DIR / f"{spec_id}.md"
            if not spec_file.exists():
                logger.debug(f"Spec not found for implementation: {spec_id}")
                continue

            file_path = f"plots/{library}/{plot_function}/{spec_id}/{variant}.py"
            implementations.append({
                "spec_id": spec_id,
                "library_id": library,
                "plot_function": plot_function,
                "variant": variant,
                "file_path": file_path,
            })

    return implementations


def get_gcs_preview_url(spec_id: str, library: str, variant: str = "default") -> str | None:
    """
    Get the GCS preview URL for an implementation.

    The URL pattern is: gs://{bucket}/plots/{spec_id}/{library}/{variant}/v{timestamp}.png
    We return the public URL format.

    Args:
        spec_id: The specification ID
        library: The library name
        variant: The variant name (default: "default")

    Returns:
        Public GCS URL or None if not available
    """
    # We construct the base path - the actual latest file will be determined
    # by the API when serving images. For now, we store the base pattern.
    # The gen-preview workflow uploads with timestamps, so we use the pattern.
    base_url = f"https://storage.googleapis.com/{GCS_BUCKET}/plots/{spec_id}/{library}/{variant}/"
    return base_url


async def sync_to_database(session: AsyncSession, specs: list[dict], implementations: list[dict]) -> dict:
    """
    Sync specs and implementations to the database.

    Performs upserts and removes entries that no longer exist in the repo.

    Args:
        session: Database session
        specs: List of spec dictionaries
        implementations: List of implementation dictionaries

    Returns:
        Dict with counts of synced/removed items
    """
    stats = {"specs_synced": 0, "specs_removed": 0, "impls_synced": 0, "impls_removed": 0}

    # Ensure libraries exist
    for lib_data in LIBRARIES_SEED:
        stmt = insert(Library).values(**lib_data).on_conflict_do_nothing(index_elements=["id"])
        await session.execute(stmt)

    # Upsert specs
    spec_ids = set()
    for spec_data in specs:
        spec_ids.add(spec_data["id"])
        stmt = insert(Spec).values(**spec_data).on_conflict_do_update(
            index_elements=["id"],
            set_={
                "title": spec_data["title"],
                "description": spec_data["description"],
                "data_requirements": spec_data["data_requirements"],
                "tags": spec_data["tags"],
            },
        )
        await session.execute(stmt)
        stats["specs_synced"] += 1

    # Remove specs that no longer exist in repo
    result = await session.execute(select(Spec.id).where(Spec.id.notin_(spec_ids)))
    removed_spec_ids = [row[0] for row in result.fetchall()]
    if removed_spec_ids:
        await session.execute(delete(Spec).where(Spec.id.in_(removed_spec_ids)))
        stats["specs_removed"] = len(removed_spec_ids)
        logger.info(f"Removed {len(removed_spec_ids)} specs no longer in repo")

    # Upsert implementations
    impl_keys = set()
    for impl_data in implementations:
        key = (impl_data["spec_id"], impl_data["library_id"], impl_data["variant"])
        impl_keys.add(key)

        # Add preview URL
        impl_data["preview_url"] = get_gcs_preview_url(
            impl_data["spec_id"], impl_data["library_id"], impl_data["variant"]
        )

        stmt = insert(Implementation).values(**impl_data).on_conflict_do_update(
            constraint="uq_implementation",
            set_={
                "plot_function": impl_data["plot_function"],
                "file_path": impl_data["file_path"],
                "preview_url": impl_data["preview_url"],
            },
        )
        await session.execute(stmt)
        stats["impls_synced"] += 1

    # Remove implementations that no longer exist in repo
    result = await session.execute(
        select(Implementation.spec_id, Implementation.library_id, Implementation.variant)
    )
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
    logger.info(f"Specs directory: {SPECS_DIR}")
    logger.info(f"Plots directory: {PLOTS_DIR}")

    # Parse all specs
    specs = []
    excluded = {".template", "VERSIONING"}
    for spec_file in SPECS_DIR.glob("*.md"):
        if spec_file.stem in excluded:
            continue
        try:
            spec_data = parse_spec_markdown(spec_file)
            specs.append(spec_data)
            logger.debug(f"Parsed spec: {spec_data['id']}")
        except Exception as e:
            logger.error(f"Failed to parse {spec_file}: {e}")

    logger.info(f"Found {len(specs)} specs")

    # Scan implementations
    implementations = scan_implementations()
    logger.info(f"Found {len(implementations)} implementations")

    # Create database connection
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with async_session() as session:
            stats = await sync_to_database(session, specs, implementations)

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
