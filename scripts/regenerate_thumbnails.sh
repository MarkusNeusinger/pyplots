#!/bin/bash
# Regenerate all thumbnails with parallel processing

set -e

PARALLEL_JOBS=10

process_image() {
    local url="$1"
    local tmpdir=$(mktemp -d)

    # Extract spec and library from URL
    # gs://pyplots-images/plots/area-basic/altair/plot.png
    local spec=$(echo "$url" | cut -d'/' -f5)
    local lib=$(echo "$url" | cut -d'/' -f6)
    local thumb_url="${url/plot.png/plot_thumb.png}"

    # Download
    gsutil -q cp "$url" "$tmpdir/plot.png" 2>/dev/null

    # Generate 1200px thumbnail
    python3 -c "
from PIL import Image
img = Image.open('$tmpdir/plot.png')
ratio = 1200 / img.width
new_size = (1200, int(img.height * ratio))
thumb = img.resize(new_size, Image.Resampling.LANCZOS)
thumb.save('$tmpdir/thumb.png', optimize=True)
print(f'{new_size[0]}x{new_size[1]}')
" 2>/dev/null

    # Upload
    gsutil -q cp "$tmpdir/thumb.png" "$thumb_url" 2>/dev/null
    gsutil -q acl ch -u AllUsers:R "$thumb_url" 2>/dev/null || true

    # Cleanup
    rm -rf "$tmpdir"

    echo "OK: $spec/$lib"
}

export -f process_image

echo "Listing images..."
urls=$(gsutil ls "gs://pyplots-images/plots/**/plot.png")
total=$(echo "$urls" | wc -l)
echo "Found $total images, processing with $PARALLEL_JOBS parallel jobs..."

echo "$urls" | xargs -P $PARALLEL_JOBS -I {} bash -c 'process_image "$@"' _ {}

echo ""
echo "Done!"
