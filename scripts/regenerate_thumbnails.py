#!/usr/bin/env python3
"""Regenerate all thumbnails in GCS with new 1200px resolution.

Usage:
    python scripts/regenerate_thumbnails.py [--dry-run]
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for core imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.images import create_thumbnail


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def main(dry_run: bool = False):
    # List all plot.png files in GCS
    print("Listing plot images in GCS...")
    result = run_cmd(["gsutil", "ls", "gs://pyplots-images/plots/**/plot.png"])
    plot_urls = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

    print(f"Found {len(plot_urls)} images to process")

    if dry_run:
        print("\n[DRY RUN] Would regenerate thumbnails for:")
        for url in plot_urls[:10]:
            print(f"  {url}")
        if len(plot_urls) > 10:
            print(f"  ... and {len(plot_urls) - 10} more")
        return

    success = 0
    failed = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        for i, plot_url in enumerate(plot_urls, 1):
            # Extract path info
            # gs://pyplots-images/plots/area-basic/altair/plot.png
            parts = plot_url.replace("gs://pyplots-images/", "").split("/")
            spec_id = parts[1]  # area-basic
            library = parts[2]  # altair

            thumb_url = plot_url.replace("/plot.png", "/plot_thumb.png")

            print(f"[{i}/{len(plot_urls)}] {spec_id}/{library}...", end=" ", flush=True)

            try:
                # Download original
                local_plot = tmpdir / "plot.png"
                local_thumb = tmpdir / "plot_thumb.png"

                run_cmd(["gsutil", "cp", plot_url, str(local_plot)])

                # Generate thumbnail at 1200px
                w, h = create_thumbnail(local_plot, local_thumb, width=1200)

                # Upload thumbnail
                run_cmd(["gsutil", "cp", str(local_thumb), thumb_url])
                run_cmd(["gsutil", "acl", "ch", "-u", "AllUsers:R", thumb_url], check=False)

                print(f"OK ({w}x{h})")
                success += 1

            except Exception as e:
                print(f"FAILED: {e}")
                failed += 1

    print(f"\nDone! Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
