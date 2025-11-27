"""Image processing utilities for pyplots.

This module provides reusable functions for image manipulation:
- Thumbnail generation with aspect ratio preservation
- Watermark application with configurable text
- PNG optimization (planned)

Usage as CLI:
    python -m core.images thumbnail input.png output.png 400
    python -m core.images watermark input.png output.png "pyplots.ai"
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Optional: pngquant for better compression
try:
    import subprocess
    _HAS_PNGQUANT = subprocess.run(
        ["pngquant", "--version"], capture_output=True
    ).returncode == 0
except (FileNotFoundError, subprocess.SubprocessError):
    _HAS_PNGQUANT = False


def create_thumbnail(
    input_path: str | Path,
    output_path: str | Path,
    width: int = 400,
    quality: int = 85,
) -> tuple[int, int]:
    """Create a thumbnail maintaining aspect ratio.

    Args:
        input_path: Path to the source image.
        output_path: Path where the thumbnail will be saved.
        width: Target width in pixels. Height is calculated to maintain aspect ratio.
        quality: JPEG quality (1-100). Only applies to JPEG output.

    Returns:
        Tuple of (width, height) of the created thumbnail.

    Raises:
        FileNotFoundError: If input_path does not exist.
        PIL.UnidentifiedImageError: If input is not a valid image.
    """
    img = Image.open(input_path)
    ratio = width / img.width
    new_size = (width, int(img.height * ratio))
    thumb = img.resize(new_size, Image.Resampling.LANCZOS)
    thumb.save(output_path, optimize=True, quality=quality)
    return new_size


def add_watermark(
    input_path: str | Path,
    output_path: str | Path,
    text: str = "pyplots.ai",
    opacity: float = 0.3,
    font_size: int = 20,
    padding: int = 10,
) -> None:
    """Add text watermark to bottom-right corner of an image.

    Args:
        input_path: Path to the source image.
        output_path: Path where the watermarked image will be saved.
        text: Watermark text to display.
        opacity: Transparency of the watermark (0.0-1.0).
        font_size: Size of the watermark font in pixels.
        padding: Padding from the image edge in pixels.

    Raises:
        FileNotFoundError: If input_path does not exist.
        PIL.UnidentifiedImageError: If input is not a valid image.
    """
    img = Image.open(input_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Try to load a nice font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    # Calculate position: bottom-right with padding
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = img.width - text_width - padding
    y = img.height - text_height - padding

    # Draw text with opacity (white text with shadow for readability)
    shadow_color = (0, 0, 0, int(255 * opacity * 0.5))
    text_color = (255, 255, 255, int(255 * opacity))

    # Shadow offset
    draw.text((x + 1, y + 1), text, font=font, fill=shadow_color)
    # Main text
    draw.text((x, y), text, font=font, fill=text_color)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(output_path, optimize=True)


def optimize_png(
    input_path: str | Path,
    output_path: str | Path | None = None,
    quality: int = 80,
) -> int:
    """Optimize PNG file size without visible quality loss.

    Uses Pillow's optimize flag, and pngquant if available for better results.

    Args:
        input_path: Path to the source PNG image.
        output_path: Path for optimized image. If None, overwrites input.
        quality: Quality level for lossy compression (1-100). Only used with pngquant.

    Returns:
        Size reduction in bytes (positive = smaller file).
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    original_size = input_path.stat().st_size

    if _HAS_PNGQUANT:
        # pngquant gives much better compression
        import subprocess
        subprocess.run(
            ["pngquant", "--force", "--quality", f"{quality}-100",
             "--output", str(output_path), str(input_path)],
            check=True
        )
    else:
        # Fallback: Pillow optimize
        img = Image.open(input_path)
        img.save(output_path, optimize=True)

    new_size = output_path.stat().st_size
    return original_size - new_size


def process_plot_image(
    input_path: str | Path,
    output_path: str | Path,
    thumb_path: str | Path | None = None,
    thumb_width: int = 400,
    watermark_text: str = "pyplots.ai",
    add_watermark_flag: bool = True,
    optimize: bool = True,
) -> dict[str, str | tuple[int, int] | int]:
    """Process a plot image: add watermark, optimize, and create thumbnail.

    This is a convenience function that combines watermarking, PNG optimization,
    and thumbnail generation in a single call.

    Args:
        input_path: Path to the source plot image.
        output_path: Path for the watermarked full-size image.
        thumb_path: Path for the thumbnail. If None, no thumbnail is created.
        thumb_width: Width of the thumbnail in pixels.
        watermark_text: Text for the watermark.
        add_watermark_flag: Whether to add a watermark.
        optimize: Whether to optimize PNG file size.

    Returns:
        Dictionary with processing results:
        - 'output': Path to the output image
        - 'thumbnail': Path to thumbnail (if created)
        - 'thumb_size': Tuple of thumbnail dimensions (if created)
        - 'bytes_saved': Bytes saved by optimization (if optimized)
    """
    result: dict[str, str | tuple[int, int] | int] = {"output": str(output_path)}

    if add_watermark_flag:
        add_watermark(input_path, output_path, text=watermark_text)
    else:
        # Just copy the image with optimization
        img = Image.open(input_path)
        img.save(output_path, optimize=True)

    # Optimize PNG
    if optimize:
        bytes_saved = optimize_png(output_path)
        result["bytes_saved"] = bytes_saved

    if thumb_path:
        # Create thumbnail from the processed image
        thumb_size = create_thumbnail(output_path, thumb_path, width=thumb_width)
        result["thumbnail"] = str(thumb_path)
        result["thumb_size"] = thumb_size

    return result


if __name__ == "__main__":
    import sys

    def print_usage() -> None:
        print("Usage:")
        print("  python -m core.images thumbnail <input> <output> [width]")
        print("  python -m core.images watermark <input> <output> [text]")
        print("  python -m core.images process <input> <output> <thumb> [watermark_text]")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_usage()

    command = sys.argv[1]

    if command == "thumbnail":
        if len(sys.argv) < 4:
            print_usage()
        input_path, output_path = sys.argv[2], sys.argv[3]
        width = int(sys.argv[4]) if len(sys.argv) > 4 else 400
        w, h = create_thumbnail(input_path, output_path, width)
        print(f"Thumbnail: {w}x{h}px")

    elif command == "watermark":
        if len(sys.argv) < 4:
            print_usage()
        input_path, output_path = sys.argv[2], sys.argv[3]
        text = sys.argv[4] if len(sys.argv) > 4 else "pyplots.ai"
        add_watermark(input_path, output_path, text)
        print(f"Watermark added: {text}")

    elif command == "process":
        if len(sys.argv) < 5:
            print_usage()
        input_path, output_path, thumb_path = sys.argv[2], sys.argv[3], sys.argv[4]
        text = sys.argv[5] if len(sys.argv) > 5 else "pyplots.ai"
        result = process_plot_image(input_path, output_path, thumb_path, watermark_text=text)
        print(f"Processed: {result}")

    else:
        print(f"Unknown command: {command}")
        print_usage()
