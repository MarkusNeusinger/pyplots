#!/usr/bin/env python3
"""
Sync plots from repository to PostgreSQL.

This script is run by GitHub Actions on push to main branch.
It ensures the database only contains data for code that is actually in main.

New structure (plots/{specification_id}/):
- specification.md: Spec description, data requirements, use cases
- specification.yaml: Spec-level metadata (tags, created, issue, suggested, updates)
- metadata/{library}.yaml: Per-library metadata (preview_url, quality_score, history)
- implementations/{library}.py: Library-specific implementation code

Legacy structure (still supported during migration):
- spec.md + metadata.yaml (single file with all library metadata)
"""

import asyncio
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv


load_dotenv()

from sqlalchemy import delete, select  # noqa: E402
from sqlalchemy.dialects.postgresql import insert  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

from core.database import LIBRARIES_SEED, Impl, Library, Spec  # noqa: E402
from core.database.connection import close_db, get_db_context, init_db, is_db_configured  # noqa: E402


# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
PLOTS_DIR = BASE_DIR / "plots"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def convert_datetimes_to_strings(obj):
    """Recursively convert datetime objects to ISO strings for JSON serialization."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_datetimes_to_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes_to_strings(item) for item in obj]
    return obj


def parse_bullet_points(text: str) -> list[str]:
    """Extract bullet points from a markdown section."""
    bullets = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets


def parse_spec_markdown(file_path: Path) -> dict:
    """
    Parse a spec.md file and extract metadata.

    Args:
        file_path: Path to the spec.md file

    Returns:
        Dict with title, description, applications, data, notes
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

    # Parse applications section (bullet points)
    applications = []
    apps_match = re.search(r"## Applications\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if apps_match:
        applications = parse_bullet_points(apps_match.group(1))

    # Parse data section (bullet points)
    data = []
    data_match = re.search(r"## Data\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if data_match:
        data = parse_bullet_points(data_match.group(1))

    # Parse notes section (bullet points, optional)
    notes = []
    notes_match = re.search(r"## Notes\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if notes_match:
        notes = parse_bullet_points(notes_match.group(1))

    return {
        "id": spec_id,
        "title": title,
        "description": description,
        "applications": applications,
        "data": data,
        "notes": notes,
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
        # Accept both spec_id and specification_id (for backwards compatibility)
        if not data or ("spec_id" not in data and "specification_id" not in data):
            return None
        return data
    except Exception as e:
        logger.error(f"Failed to parse metadata {file_path}: {e}")
        return None


def parse_library_metadata_yaml(file_path: Path) -> dict | None:
    """
    Parse a per-library metadata/{library}.yaml file.

    Args:
        file_path: Path to the metadata file (e.g., metadata/matplotlib.yaml)

    Returns:
        Dict with library metadata or None if invalid
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if not data or "library" not in data:
            return None
        return data
    except Exception as e:
        logger.error(f"Failed to parse library metadata {file_path}: {e}")
        return None


def scan_plot_directory(plot_dir: Path) -> dict | None:
    """
    Scan a single plot directory and extract all data.

    Supports both new structure (specification.md + specification.yaml + metadata/*.yaml)
    and legacy structure (spec.md + metadata.yaml) during migration.

    Args:
        plot_dir: Path to the plot directory (e.g., plots/scatter-basic/)

    Returns:
        Dict with spec data, metadata, and implementations
    """
    spec_id = plot_dir.name
    implementations_dir = plot_dir / "implementations"
    metadata_dir = plot_dir / "metadata"

    # Support both new (specification.md) and legacy (spec.md) file names
    spec_file = plot_dir / "specification.md"
    if not spec_file.exists():
        spec_file = plot_dir / "spec.md"  # Legacy fallback

    # Support both new (specification.yaml) and legacy (metadata.yaml) file names
    spec_metadata_file = plot_dir / "specification.yaml"
    legacy_metadata_file = plot_dir / "metadata.yaml"

    if not spec_file.exists():
        logger.warning(f"No specification.md or spec.md found in {plot_dir}")
        return None

    # Parse spec
    spec_data = parse_spec_markdown(spec_file)

    # Parse spec-level metadata (new structure: specification.yaml, legacy: metadata.yaml)
    metadata = {}
    if spec_metadata_file.exists():
        metadata = parse_metadata_yaml(spec_metadata_file) or {}
    elif legacy_metadata_file.exists():
        metadata = parse_metadata_yaml(legacy_metadata_file) or {}

    # Merge title from metadata if available
    if metadata.get("title"):
        spec_data["title"] = metadata["title"]

    # Add spec-level metadata from YAML (convert datetimes in JSONB fields)
    spec_data["tags"] = convert_datetimes_to_strings(metadata.get("tags"))
    spec_data["history"] = convert_datetimes_to_strings(metadata.get("history"))
    spec_data["issue"] = metadata.get("issue")
    spec_data["suggested"] = metadata.get("suggested")

    # Parse created timestamp (convert to naive datetime for DB)
    # YAML auto-parses dates, so datetime comes first
    created = metadata.get("created")
    if isinstance(created, datetime):
        spec_data["created"] = created.replace(tzinfo=None) if created.tzinfo else created
    elif isinstance(created, str):
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            spec_data["created"] = dt.replace(tzinfo=None)
        except ValueError:
            spec_data["created"] = None
    else:
        spec_data["created"] = None

    # Scan implementations
    implementations = []
    if implementations_dir.exists():
        for impl_file in implementations_dir.glob("*.py"):
            if impl_file.name.startswith("_"):
                continue

            library_id = impl_file.stem  # e.g., "matplotlib", "seaborn"
            code = impl_file.read_text(encoding="utf-8")

            # Get implementation metadata from per-library file (new) or legacy metadata.yaml
            impl_meta = {}
            library_metadata_file = metadata_dir / f"{library_id}.yaml"
            if library_metadata_file.exists():
                # New structure: metadata/{library}.yaml
                impl_meta = parse_library_metadata_yaml(library_metadata_file) or {}
            else:
                # Legacy structure: metadata.yaml -> implementations -> {library}
                impl_meta = metadata.get("implementations", {}).get(library_id, {})

            current = impl_meta.get("current") or {}

            # Parse generated_at (strip timezone for DB compatibility)
            generated_at = current.get("generated_at")
            if isinstance(generated_at, str):
                try:
                    dt = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
                    generated_at = dt.replace(tzinfo=None)  # Remove timezone info
                except ValueError:
                    generated_at = None
            elif isinstance(generated_at, datetime):
                generated_at = generated_at.replace(tzinfo=None)

            implementations.append(
                {
                    "spec_id": spec_id,
                    "library_id": library_id,
                    "code": code,
                    # Preview URLs (from metadata YAML, filled by workflow)
                    "preview_url": impl_meta.get("preview_url"),
                    "preview_thumb": impl_meta.get("preview_thumb"),
                    "preview_html": impl_meta.get("preview_html"),
                    # Versions (from metadata YAML, filled by workflow)
                    "python_version": current.get("python_version"),
                    "library_version": current.get("library_version"),
                    # Generation metadata
                    "generated_at": generated_at,
                    "generated_by": current.get("generated_by"),
                    "workflow_run": current.get("workflow_run"),
                    "issue": current.get("issue"),
                    "quality_score": current.get("quality_score"),
                    # Quality evaluation details (convert datetimes in JSONB)
                    "evaluator_scores": convert_datetimes_to_strings(current.get("evaluator_scores")),
                    "quality_feedback": current.get("quality_feedback"),
                    "improvements_suggested": convert_datetimes_to_strings(current.get("improvements_suggested")),
                    # Version history (convert datetimes in JSONB)
                    "history": convert_datetimes_to_strings(impl_meta.get("history")),
                }
            )

    return {"spec": spec_data, "implementations": implementations}


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
                    "applications": spec["applications"],
                    "data": spec["data"],
                    "notes": spec["notes"],
                    "created": spec.get("created"),
                    "issue": spec.get("issue"),
                    "suggested": spec.get("suggested"),
                    "tags": spec.get("tags"),
                    "history": spec.get("history"),
                },
            )
        )
        await session.execute(stmt)
        stats["specs_synced"] += 1

        # Upsert implementations
        for impl in plot_data["implementations"]:
            key = (impl["spec_id"], impl["library_id"])
            impl_keys.add(key)

            update_set = {"code": impl["code"]}

            # Add optional fields (only if not None)
            optional_fields = [
                "preview_url",
                "preview_thumb",
                "preview_html",
                "python_version",
                "library_version",
                "generated_at",
                "generated_by",
                "workflow_run",
                "issue",
                "quality_score",
                "evaluator_scores",
                "quality_feedback",
                "improvements_suggested",
                "history",
            ]
            for field in optional_fields:
                if impl.get(field) is not None:
                    update_set[field] = impl[field]

            stmt = insert(Impl).values(**impl).on_conflict_do_update(constraint="uq_impl", set_=update_set)
            await session.execute(stmt)
            stats["impls_synced"] += 1

    # Remove specs that no longer exist in repo
    result = await session.execute(select(Spec.id).where(Spec.id.notin_(spec_ids)))
    removed_spec_ids = [row[0] for row in result.fetchall()]
    if removed_spec_ids:
        await session.execute(delete(Spec).where(Spec.id.in_(removed_spec_ids)))
        stats["specs_removed"] = len(removed_spec_ids)
        logger.info(f"Removed {len(removed_spec_ids)} specs no longer in repo")

    # Remove impls that no longer exist in repo
    result = await session.execute(select(Impl.spec_id, Impl.library_id))
    existing_impls = [(row[0], row[1]) for row in result.fetchall()]

    removed_impls = [impl for impl in existing_impls if impl not in impl_keys]
    if removed_impls:
        for spec_id, library_id in removed_impls:
            await session.execute(delete(Impl).where(Impl.spec_id == spec_id, Impl.library_id == library_id))
        stats["impls_removed"] = len(removed_impls)
        logger.info(f"Removed {len(removed_impls)} impls no longer in repo")

    await session.commit()
    return stats


async def main() -> int:
    """Main entry point for the sync script."""
    if not is_db_configured():
        logger.error("No database configuration found (DATABASE_URL or INSTANCE_CONNECTION_NAME)")
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

    # Initialize database connection (uses Cloud SQL Connector if INSTANCE_CONNECTION_NAME is set)
    try:
        await init_db()
        async with get_db_context() as session:
            stats = await sync_to_database(session, plots)

        logger.info("Sync completed successfully!")
        logger.info(f"  Specs synced: {stats['specs_synced']}, removed: {stats['specs_removed']}")
        logger.info(f"  Implementations synced: {stats['impls_synced']}, removed: {stats['impls_removed']}")
        return 0

    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return 1

    finally:
        await close_db()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
