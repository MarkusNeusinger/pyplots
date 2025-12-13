"""Image processing utilities for pyplots.

This module provides reusable functions for image manipulation:
- Thumbnail generation with aspect ratio preservation
- PNG optimization with pngquant

Usage as CLI:
    python -m core.images thumbnail input.png output.png 400
    python -m core.images process input.png output.png thumb.png
"""

from pathlib import Path

from PIL import Image


# Brand colors from website (kept for potential future use)
PYPLOTS_BLUE = "#3776AB"  # Python blue
PYPLOTS_YELLOW = "#FFD43B"  # Python yellow
PYPLOTS_DARK = "#1f2937"  # Dark gray

# Optional: pngquant for better compression
try:
    import subprocess

    _HAS_PNGQUANT = subprocess.run(["pngquant", "--version"], capture_output=True).returncode == 0
except (FileNotFoundError, subprocess.SubprocessError):
    _HAS_PNGQUANT = False


def create_thumbnail(input_path: str | Path, output_path: str | Path, width: int = 600) -> tuple[int, int]:
    """Create a thumbnail maintaining aspect ratio.

    Args:
        input_path: Path to the source image.
        output_path: Path where the thumbnail will be saved.
        width: Target width in pixels (default: 600). Height is calculated to maintain aspect ratio.

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
    thumb.save(output_path, optimize=True)
    return new_size


def optimize_png(input_path: str | Path, output_path: str | Path | None = None, quality: int = 80) -> int:
    """Optimize PNG file size using pngquant (if available) or Pillow.

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
        import subprocess

        subprocess.run(
            ["pngquant", "--force", "--quality", f"{quality}-100", "--output", str(output_path), str(input_path)],
            check=True,
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
    thumb_width: int = 600,
    optimize: bool = True,
) -> dict[str, str | tuple[int, int] | int]:
    """Process a plot image: optimize and create thumbnail.

    This is the main entry point for image processing in the workflow.
    Combines PNG optimization and thumbnail generation.

    Args:
        input_path: Path to the source plot image.
        output_path: Path for the optimized full-size image.
        thumb_path: Path for the thumbnail. If None, no thumbnail is created.
        thumb_width: Width of the thumbnail in pixels.
        optimize: Whether to optimize PNG file size with pngquant.

    Returns:
        Dictionary with processing results:
        - 'output': Path to the output image
        - 'thumbnail': Path to thumbnail (if created)
        - 'thumb_size': Tuple of thumbnail dimensions (if created)
        - 'bytes_saved': Bytes saved by optimization (if optimized)
    """
    result: dict[str, str | tuple[int, int] | int] = {"output": str(output_path)}

    # Copy image (with basic Pillow optimization)
    img = Image.open(input_path)
    img.save(output_path, optimize=True)

    # Optimize PNG with pngquant
    if optimize:
        bytes_saved = optimize_png(output_path)
        result["bytes_saved"] = bytes_saved

    # Create thumbnail from the processed image
    if thumb_path:
        thumb_size = create_thumbnail(output_path, thumb_path, width=thumb_width)
        # Also optimize thumbnail
        if optimize:
            optimize_png(thumb_path)
        result["thumbnail"] = str(thumb_path)
        result["thumb_size"] = thumb_size

    return result


if __name__ == "__main__":
    import sys

    def print_usage() -> None:
        print("Usage:")
        print("  python -m core.images thumbnail <input> <output> [width]")
        print("  python -m core.images process <input> <output> [thumb]")
        print("")
        print("Examples:")
        print("  python -m core.images thumbnail plot.png thumb.png 400")
        print("  python -m core.images process plot.png out.png thumb.png")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_usage()

    command = sys.argv[1]

    if command == "thumbnail":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        width = int(sys.argv[4]) if len(sys.argv) > 4 else 600
        w, h = create_thumbnail(input_file, output_file, width)
        print(f"Thumbnail: {w}x{h}px")

    elif command == "process":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        thumb_file = sys.argv[4] if len(sys.argv) > 4 else None
        res = process_plot_image(input_file, output_file, thumb_file)
        print(f"Processed: {res}")

    else:
        print(f"Unknown command: {command}")
        print_usage()
