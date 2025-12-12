"""Image processing utilities for pyplots.

This module provides reusable functions for image manipulation:
- Thumbnail generation with aspect ratio preservation
- Watermark application with pyplots.ai branding
- PNG optimization with pngquant

Usage as CLI:
    python -m core.images thumbnail input.png output.png 400
    python -m core.images watermark input.png output.png scatter-basic
    python -m core.images process input.png output.png thumb.png scatter-basic
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# Brand colors from website
PYPLOTS_BLUE = "#3776AB"  # Python blue - for "py" and spec_id
PYPLOTS_YELLOW = "#FFD43B"  # Python yellow - for "plots"
PYPLOTS_DARK = "#1f2937"  # Dark gray - for ".ai"

# Optional: pngquant for better compression
try:
    import subprocess

    _HAS_PNGQUANT = subprocess.run(["pngquant", "--version"], capture_output=True).returncode == 0
except (FileNotFoundError, subprocess.SubprocessError):
    _HAS_PNGQUANT = False


def _hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    """Convert hex color to RGBA tuple."""
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def _get_font(font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load JetBrains Mono Bold font, with fallbacks."""
    font_paths = [
        "JetBrainsMono-Bold.ttf",  # Local file
        "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf",
        "/tmp/JetBrainsMono-Bold.ttf",  # Downloaded by workflow
        "DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    return ImageFont.load_default()


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


def add_watermark(
    input_path: str | Path,
    output_path: str | Path,
    spec_id: str | None = None,
    font_size: int | None = None,
    padding: int | None = None,
) -> None:
    """Add pyplots.ai branded watermark to an image.

    Adds pyplots.ai (in brand colors) to bottom-right and spec_id to bottom-left.
    Uses JetBrains Mono Bold font with gray shadow for readability.
    Font size and padding scale automatically based on image width.

    Args:
        input_path: Path to the source image.
        output_path: Path where the watermarked image will be saved.
        spec_id: Spec ID for bottom-left corner (e.g., "scatter-basic").
        font_size: Size of the watermark font in pixels. If None, auto-scales (~1% of width).
        padding: Padding from the image edge in pixels. If None, auto-scales (~0.5% of width).

    Raises:
        FileNotFoundError: If input_path does not exist.
        PIL.UnidentifiedImageError: If input is not a valid image.
    """
    img = Image.open(input_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Auto-scale font size and padding based on image width
    if font_size is None:
        font_size = max(24, int(img.width * 0.0135))  # ~1.35% of width, min 24px
    if padding is None:
        padding = max(15, int(img.width * 0.008))  # ~0.8% of width, min 15px

    font = _get_font(font_size)
    alpha = int(255 * 0.95)

    # Brand colors
    py_color = _hex_to_rgba(PYPLOTS_BLUE, alpha)
    plots_color = _hex_to_rgba(PYPLOTS_YELLOW, alpha)
    ai_color = _hex_to_rgba(PYPLOTS_DARK, alpha)
    shadow_color = (50, 50, 50, 150)  # Gray shadow

    # Measure text dimensions
    py_w = draw.textbbox((0, 0), "py", font=font)[2]
    plots_w = draw.textbbox((0, 0), "plots", font=font)[2]
    ai_w = draw.textbbox((0, 0), ".ai", font=font)[2]
    url_w = py_w + plots_w + ai_w
    text_h = draw.textbbox((0, 0), "py", font=font)[3]

    # Position: bottom with padding
    y = img.height - text_h - padding
    url_x = img.width - url_w - padding
    spec_x = padding
    shadow_offset = 2

    # Draw pyplots.ai with shadow (right side)
    # Shadow first
    draw.text((url_x + shadow_offset, y + shadow_offset), "py", font=font, fill=shadow_color)
    draw.text((url_x + py_w + shadow_offset, y + shadow_offset), "plots", font=font, fill=shadow_color)
    draw.text((url_x + py_w + plots_w + shadow_offset, y + shadow_offset), ".ai", font=font, fill=shadow_color)
    # Colored text
    draw.text((url_x, y), "py", font=font, fill=py_color)
    draw.text((url_x + py_w, y), "plots", font=font, fill=plots_color)
    draw.text((url_x + py_w + plots_w, y), ".ai", font=font, fill=ai_color)

    # Draw spec_id with shadow (left side)
    if spec_id:
        draw.text((spec_x + shadow_offset, y + shadow_offset), spec_id, font=font, fill=shadow_color)
        draw.text((spec_x, y), spec_id, font=font, fill=py_color)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(output_path, optimize=True)


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
    spec_id: str | None = None,
    add_watermark_flag: bool = True,
    optimize: bool = True,
) -> dict[str, str | tuple[int, int] | int]:
    """Process a plot image: add watermark, optimize, and create thumbnail.

    This is the main entry point for image processing in the workflow.
    Combines watermarking, PNG optimization, and thumbnail generation.

    Args:
        input_path: Path to the source plot image.
        output_path: Path for the watermarked full-size image.
        thumb_path: Path for the thumbnail. If None, no thumbnail is created.
        thumb_width: Width of the thumbnail in pixels.
        spec_id: Spec ID for bottom-left watermark (e.g., "scatter-basic").
        add_watermark_flag: Whether to add a watermark.
        optimize: Whether to optimize PNG file size with pngquant.

    Returns:
        Dictionary with processing results:
        - 'output': Path to the output image
        - 'thumbnail': Path to thumbnail (if created)
        - 'thumb_size': Tuple of thumbnail dimensions (if created)
        - 'bytes_saved': Bytes saved by optimization (if optimized)
    """
    result: dict[str, str | tuple[int, int] | int] = {"output": str(output_path)}

    if add_watermark_flag:
        add_watermark(input_path, output_path, spec_id=spec_id)
    else:
        # Just copy the image with optimization
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


def add_html_watermark(html_content: str, spec_id: str) -> str:
    """Add pyplots.ai watermark footer to HTML chart.

    Adds a branded footer with spec_id (left) and pyplots.ai (right) using
    JetBrains Mono font and brand colors. The chart and watermark are wrapped
    in a container to prevent layout issues on resize.

    Args:
        html_content: HTML content string (e.g., from Altair, Plotly, Bokeh).
        spec_id: Spec ID for the left side (e.g., "scatter-basic").

    Returns:
        HTML string with watermark added.

    Note:
        Works with HTML files that have a <div id="vis"></div> element.
        The watermark uses Google Fonts CDN for JetBrains Mono.
    """
    watermark_css = """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&display=swap');
      body {
        margin: 0;
        padding: 0;
      }
      .pyplots-container {
        display: inline-block;
        position: relative;
      }
      .pyplots-watermark {
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 14px;
        background: #fff;
      }
      .pyplots-watermark .spec-id {
        color: #3776AB;
      }
      .pyplots-watermark .brand .py { color: #3776AB; }
      .pyplots-watermark .brand .plots { color: #FFD43B; }
      .pyplots-watermark .brand .ai { color: #1f2937; }
    </style>
    """

    watermark_html = f"""<div class="pyplots-container">
      <div id="vis"></div>
      <div class="pyplots-watermark">
        <span class="spec-id">{spec_id}</span>
        <span class="brand"><span class="py">py</span><span class="plots">plots</span><span class="ai">.ai</span></span>
      </div>
    </div>"""

    # Replace the vis div with container + watermark
    html_content = html_content.replace('<div id="vis"></div>', watermark_html)

    # Insert CSS before </head>
    html_content = html_content.replace("</head>", watermark_css + "</head>")

    return html_content


if __name__ == "__main__":
    import sys

    def print_usage() -> None:
        print("Usage:")
        print("  python -m core.images thumbnail <input> <output> [width]")
        print("  python -m core.images watermark <input> <output> [spec_id]")
        print("  python -m core.images html-watermark <input> <output> <spec_id>")
        print("  python -m core.images process <input> <output> <thumb> [spec_id]")
        print("")
        print("Examples:")
        print("  python -m core.images process plot.png out.png thumb.png scatter-basic")
        print("  python -m core.images html-watermark chart.html out.html scatter-basic")
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

    elif command == "watermark":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        spec = sys.argv[4] if len(sys.argv) > 4 else None
        add_watermark(input_file, output_file, spec_id=spec)
        print(f"Watermark added (spec_id={spec})")

    elif command == "html-watermark":
        if len(sys.argv) < 5:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        spec = sys.argv[4]
        with open(input_file) as f:
            html = f.read()
        result = add_html_watermark(html, spec)
        with open(output_file, "w") as f:
            f.write(result)
        print(f"HTML watermark added (spec_id={spec})")

    elif command == "process":
        if len(sys.argv) < 5:
            print_usage()
        input_file, output_file, thumb_file = sys.argv[2], sys.argv[3], sys.argv[4]
        spec = sys.argv[5] if len(sys.argv) > 5 else None
        res = process_plot_image(input_file, output_file, thumb_file, spec_id=spec)
        print(f"Processed: {res}")

    else:
        print(f"Unknown command: {command}")
        print_usage()
