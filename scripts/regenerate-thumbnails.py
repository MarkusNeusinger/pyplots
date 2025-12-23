#!/usr/bin/env python3
"""Regenerate thumbnails for implementations that went through repair loops.

These implementations have mismatched thumbnails because impl-repair.yml
didn't regenerate thumbnails during repairs.

Usage:
    python scripts/regenerate-thumbnails.py [--dry-run]
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.images import process_plot_image


def get_affected_implementations():
    """Find implementations where created != updated (went through repairs)."""
    plots_dir = Path("plots")
    affected = []

    for spec_dir in plots_dir.iterdir():
        if not spec_dir.is_dir():
            continue
        metadata_dir = spec_dir / "metadata"
        if not metadata_dir.exists():
            continue

        for lib_file in metadata_dir.glob("*.yaml"):
            try:
                with open(lib_file) as f:
                    data = yaml.safe_load(f)

                created = str(data.get("created", ""))
                updated = str(data.get("updated", ""))

                # Only include if they went through repairs
                if created and updated and created != updated:
                    spec_id = spec_dir.name
                    library = lib_file.stem
                    affected.append((spec_id, library))
            except Exception:
                pass

    return sorted(affected)


def regenerate_thumbnail(spec_id: str, library: str, dry_run: bool = False) -> bool:
    """Download plot.png, regenerate thumbnail, upload to GCS."""
    gcs_base = f"gs://pyplots-images/plots/{spec_id}/{library}"
    public_base = f"https://storage.googleapis.com/pyplots-images/plots/{spec_id}/{library}"

    with tempfile.TemporaryDirectory() as tmpdir:
        plot_path = Path(tmpdir) / "plot.png"
        thumb_path = Path(tmpdir) / "plot_thumb.png"

        # Download plot.png
        result = subprocess.run(
            ["gsutil", "cp", f"{gcs_base}/plot.png", str(plot_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"  ERROR: Failed to download plot.png: {result.stderr}")
            return False

        if not plot_path.exists():
            print(f"  ERROR: plot.png not found after download")
            return False

        # Generate thumbnail
        try:
            process_plot_image(str(plot_path), str(plot_path), str(thumb_path))
        except Exception as e:
            print(f"  ERROR: Failed to generate thumbnail: {e}")
            return False

        if not thumb_path.exists():
            print(f"  ERROR: Thumbnail not created")
            return False

        # Upload thumbnail
        if dry_run:
            print(f"  DRY-RUN: Would upload {thumb_path} to {gcs_base}/plot_thumb.png")
            return True

        result = subprocess.run(
            ["gsutil", "cp", str(thumb_path), f"{gcs_base}/plot_thumb.png"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"  ERROR: Failed to upload thumbnail: {result.stderr}")
            return False

        # Make public
        subprocess.run(
            ["gsutil", "acl", "ch", "-u", "AllUsers:R", f"{gcs_base}/plot_thumb.png"],
            capture_output=True,
        )

        print(f"  OK: {public_base}/plot_thumb.png")
        return True


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("DRY RUN MODE - no changes will be made\n")

    # Check gsutil is available
    result = subprocess.run(["gsutil", "version"], capture_output=True)
    if result.returncode != 0:
        print("ERROR: gsutil not found. Please install Google Cloud SDK.")
        sys.exit(1)

    affected = get_affected_implementations()
    print(f"Found {len(affected)} implementations that went through repairs\n")

    success = 0
    failed = 0

    for spec_id, library in affected:
        print(f"Processing {spec_id}/{library}...")
        if regenerate_thumbnail(spec_id, library, dry_run):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} succeeded, {failed} failed")


if __name__ == "__main__":
    main()
