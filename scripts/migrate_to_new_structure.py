#!/usr/bin/env python3
"""
Migrate plots from legacy structure to new structure.

Legacy structure:
- spec.md
- metadata.yaml (monolithic with all library data)

New structure:
- specification.md
- specification.yaml (spec-level only: tags, created, issue, suggested, updates)
- metadata/{library}.yaml (per-library: preview_url, current, history)

Usage:
    python scripts/migrate_to_new_structure.py [--dry-run]
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

import yaml


# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
PLOTS_DIR = BASE_DIR / "plots"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def migrate_plot_directory(plot_dir: Path, dry_run: bool = False) -> bool:
    """
    Migrate a single plot directory to new structure.

    Args:
        plot_dir: Path to the plot directory
        dry_run: If True, only log what would be done

    Returns:
        True if migration successful, False otherwise
    """
    spec_id = plot_dir.name
    logger.info(f"Migrating: {spec_id}")

    # Check if already migrated
    if (plot_dir / "specification.md").exists():
        logger.info("  Already migrated (specification.md exists)")
        return True

    # Check for legacy files
    legacy_spec = plot_dir / "spec.md"
    legacy_metadata = plot_dir / "metadata.yaml"

    if not legacy_spec.exists():
        logger.warning("  No spec.md found, skipping")
        return False

    # Step 1: Rename spec.md -> specification.md
    new_spec = plot_dir / "specification.md"
    if dry_run:
        logger.info("  [DRY RUN] Would rename: spec.md -> specification.md")
    else:
        shutil.move(legacy_spec, new_spec)
        logger.info("  Renamed: spec.md -> specification.md")

    # Step 2: Split metadata.yaml
    if not legacy_metadata.exists():
        logger.info("  No metadata.yaml found, creating empty specification.yaml")
        if not dry_run:
            spec_yaml = {
                "specification_id": spec_id,
                "title": spec_id.replace("-", " ").title(),
                "created": None,
                "issue": None,
                "suggested": None,
                "updates": [],
                "tags": {
                    "plot_type": [],
                    "domain": ["general"],
                    "features": ["basic"],
                    "audience": ["beginner"],
                    "data_type": ["numeric"],
                },
            }
            with open(plot_dir / "specification.yaml", "w") as f:
                yaml.dump(spec_yaml, f, default_flow_style=False, sort_keys=False)
        return True

    # Load legacy metadata
    try:
        with open(legacy_metadata) as f:
            legacy_data = yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"  Failed to parse metadata.yaml: {e}")
        return False

    # Create specification.yaml (spec-level only)
    spec_yaml = {
        "specification_id": spec_id,
        "title": legacy_data.get("title", spec_id.replace("-", " ").title()),
        "created": legacy_data.get("created"),
        "issue": legacy_data.get("issue"),
        "suggested": legacy_data.get("suggested"),
        "updates": legacy_data.get("updates", []),
        "tags": legacy_data.get(
            "tags",
            {
                "plot_type": [],
                "domain": ["general"],
                "features": ["basic"],
                "audience": ["beginner"],
                "data_type": ["numeric"],
            },
        ),
    }

    if dry_run:
        logger.info("  [DRY RUN] Would create: specification.yaml")
    else:
        with open(plot_dir / "specification.yaml", "w") as f:
            yaml.dump(spec_yaml, f, default_flow_style=False, sort_keys=False)
        logger.info("  Created: specification.yaml")

    # Create metadata/{library}.yaml for each implementation
    implementations = legacy_data.get("implementations", {})
    if implementations:
        metadata_dir = plot_dir / "metadata"

        if dry_run:
            logger.info("  [DRY RUN] Would create: metadata/ directory")
        else:
            metadata_dir.mkdir(exist_ok=True)
            logger.info("  Created: metadata/ directory")

        for library_id, impl_data in implementations.items():
            library_yaml = {
                "library": library_id,
                "specification_id": spec_id,
                "preview_url": impl_data.get("preview_url"),
                "preview_html": impl_data.get("preview_html"),
                "current": impl_data.get("current"),
                "history": impl_data.get("history", []),
            }

            if dry_run:
                logger.info(f"  [DRY RUN] Would create: metadata/{library_id}.yaml")
            else:
                with open(metadata_dir / f"{library_id}.yaml", "w") as f:
                    yaml.dump(library_yaml, f, default_flow_style=False, sort_keys=False)
                logger.info(f"  Created: metadata/{library_id}.yaml")

    # Step 3: Delete legacy metadata.yaml
    if dry_run:
        logger.info("  [DRY RUN] Would delete: metadata.yaml")
    else:
        legacy_metadata.unlink()
        logger.info("  Deleted: metadata.yaml")

    return True


def main() -> int:
    """Main entry point for the migration script."""
    parser = argparse.ArgumentParser(description="Migrate plots to new structure")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--spec-id", type=str, help="Migrate only a specific spec ID")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Plot Structure Migration")
    logger.info("=" * 60)
    logger.info(f"Plots directory: {PLOTS_DIR}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("")

    if not PLOTS_DIR.exists():
        logger.error(f"Plots directory not found: {PLOTS_DIR}")
        return 1

    # Collect directories to migrate
    if args.spec_id:
        plot_dirs = [PLOTS_DIR / args.spec_id]
        if not plot_dirs[0].exists():
            logger.error(f"Spec not found: {args.spec_id}")
            return 1
    else:
        plot_dirs = sorted([d for d in PLOTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])

    logger.info(f"Found {len(plot_dirs)} plot directories")
    logger.info("")

    # Migrate each directory
    success_count = 0
    fail_count = 0

    for plot_dir in plot_dirs:
        try:
            if migrate_plot_directory(plot_dir, dry_run=args.dry_run):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            logger.error(f"Failed to migrate {plot_dir.name}: {e}")
            fail_count += 1

    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Migration Summary")
    logger.info("=" * 60)
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {fail_count}")
    logger.info(f"Total: {len(plot_dirs)}")

    if args.dry_run:
        logger.info("")
        logger.info("This was a DRY RUN. No changes were made.")
        logger.info("Run without --dry-run to apply changes.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
