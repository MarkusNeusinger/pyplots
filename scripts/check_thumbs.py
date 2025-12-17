#!/usr/bin/env python3
"""Check for small thumbnails and regenerate them."""
import subprocess
import sys
import tempfile
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))
from PIL import Image

from core.images import create_thumbnail


# List all thumbnails
print("Listing thumbnails...", flush=True)
result = subprocess.run(["gsutil", "ls", "gs://pyplots-images/plots/**/plot_thumb.png"],
                       capture_output=True, text=True)
thumbs = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
print(f"Found {len(thumbs)} thumbnails", flush=True)

# Check each one
small = []
with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    for i, url in enumerate(thumbs):
        local = tmpdir / "thumb.png"
        subprocess.run(["gsutil", "-q", "cp", url, str(local)], capture_output=True)
        try:
            img = Image.open(local)
            if img.width <= 600:
                spec = url.split("/")[4]
                lib = url.split("/")[5]
                small.append((url, spec, lib))
                print(f"  SMALL: {spec}/{lib} ({img.width}px)", flush=True)
        except Exception:
            pass
        if (i+1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(thumbs)}", flush=True)

print(f"\nFound {len(small)} small thumbnails", flush=True)

if small and "--fix" in sys.argv:
    print("\nRegenerating...", flush=True)
    for url, spec, lib in small:
        plot_url = url.replace("plot_thumb.png", "plot.png")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            subprocess.run(["gsutil", "-q", "cp", plot_url, str(tmpdir / "plot.png")])
            create_thumbnail(tmpdir / "plot.png", tmpdir / "thumb.png", width=1200)
            subprocess.run(["gsutil", "-q", "cp", str(tmpdir / "thumb.png"), url])
            subprocess.run(["gsutil", "-q", "acl", "ch", "-u", "AllUsers:R", url], check=False)
            print(f"  Fixed: {spec}/{lib}", flush=True)
    print("Done!", flush=True)
