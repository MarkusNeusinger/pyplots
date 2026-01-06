"""Image processing utilities for pyplots.

This module provides reusable functions for image manipulation:
- Thumbnail generation with aspect ratio preservation
- PNG optimization with pngquant
- Branded og:image generation for social media
- Collage generation for spec overview pages

Usage as CLI:
    python -m core.images thumbnail input.png output.png 400
    python -m core.images process input.png output.png thumb.png
    python -m core.images brand input.png output.png "scatter-basic" "matplotlib"
    python -m core.images collage output.png img1.png img2.png img3.png img4.png
"""

import logging
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger(__name__)

# GCS bucket for static assets (fonts)
GCS_STATIC_BUCKET = "pyplots-static"
MONOLISA_FONT_PATH = "fonts/MonoLisaVariableNormal.ttf"
FONT_CACHE_DIR = Path("/tmp/pyplots-fonts")

# Brand colors from website
PYPLOTS_BLUE = "#3776AB"  # Python blue
PYPLOTS_YELLOW = "#FFD43B"  # Python yellow
PYPLOTS_DARK = "#1f2937"  # Dark gray
PYPLOTS_BG = "#f8f9fa"  # Light background

# OG image dimensions (recommended for social media)
OG_WIDTH = 1200
OG_HEIGHT = 630
HEADER_HEIGHT = 80

# Optional: pngquant for better compression
try:
    import subprocess

    _HAS_PNGQUANT = subprocess.run(["pngquant", "--version"], capture_output=True).returncode == 0
except (FileNotFoundError, subprocess.SubprocessError):
    _HAS_PNGQUANT = False


def create_thumbnail(input_path: str | Path, output_path: str | Path, width: int = 1200) -> tuple[int, int]:
    """Create a thumbnail maintaining aspect ratio.

    Args:
        input_path: Path to the source image.
        output_path: Path where the thumbnail will be saved.
        width: Target width in pixels (default: 1200). Height is calculated to maintain aspect ratio.

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
    thumb_width: int = 1200,
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


# =============================================================================
# OG Image Branding Functions
# =============================================================================


def _get_monolisa_font_path() -> Path | None:
    """Get path to MonoLisa font, downloading from GCS if needed.

    Returns:
        Path to font file, or None if unavailable.
    """
    cached_font = FONT_CACHE_DIR / "MonoLisaVariableNormal.ttf"

    # Return cached font if exists
    if cached_font.exists():
        return cached_font

    # Try to download from GCS
    try:
        from google.cloud import storage

        FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)

        client = storage.Client()
        bucket = client.bucket(GCS_STATIC_BUCKET)
        blob = bucket.blob(MONOLISA_FONT_PATH)
        blob.download_to_filename(str(cached_font))
        logger.info(f"Downloaded MonoLisa font to {cached_font}")
        return cached_font
    except Exception as e:
        logger.warning(f"Could not load MonoLisa font from GCS: {e}")
        return None


def _get_font(size: int = 32, weight: int = 700) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Get a suitable font for text rendering.

    Tries to load MonoLisa from GCS cache, falls back to system fonts.

    Args:
        size: Font size in pixels
        weight: Font weight (100-900, default 700 for bold like website)
    """
    # Try MonoLisa first (downloaded from GCS)
    monolisa_path = _get_monolisa_font_path()
    if monolisa_path:
        try:
            font = ImageFont.truetype(str(monolisa_path), size)
            # Set variable font weight (MonoLisa supports 100-1000)
            try:
                font.set_variation_by_axes([weight])
            except Exception:
                pass  # Ignore if variation not supported
            return font
        except OSError:
            pass

    # Fallback to system fonts
    fallback_fonts = ["DejaVuSansMono-Bold.ttf", "DejaVuSansMono.ttf", "LiberationMono-Bold.ttf", "FreeMono.ttf"]

    for font_name in fallback_fonts:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue

    # Fallback to default
    return ImageFont.load_default()


def _draw_pyplots_logo(draw: ImageDraw.ImageDraw, x: int, y: int, font_size: int = 36) -> int:
    """Draw the pyplots.ai logo with proper colors.

    Args:
        draw: ImageDraw instance to draw on
        x: X coordinate for text start
        y: Y coordinate for text baseline
        font_size: Font size in pixels

    Returns:
        Total width of drawn text
    """
    font = _get_font(font_size)

    # Draw each part with its color
    parts = [("py", PYPLOTS_BLUE), ("plots", PYPLOTS_YELLOW), (".ai", PYPLOTS_DARK)]

    current_x = x
    for text, color in parts:
        draw.text((current_x, y), text, fill=color, font=font)
        bbox = draw.textbbox((current_x, y), text, font=font)
        current_x = bbox[2]  # Move to end of this text

    return current_x - x


def create_branded_header(width: int = OG_WIDTH, height: int = HEADER_HEIGHT) -> Image.Image:
    """Create a branded header strip with pyplots.ai logo.

    Args:
        width: Width of the header in pixels
        height: Height of the header in pixels

    Returns:
        PIL Image with the branded header
    """
    header = Image.new("RGB", (width, height), PYPLOTS_BG)
    draw = ImageDraw.Draw(header)

    # Center the logo
    font_size = height // 2
    font = _get_font(font_size)

    # Calculate total text width for centering
    test_text = "pyplots.ai"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 5  # Slight adjustment for visual centering

    _draw_pyplots_logo(draw, x, y, font_size)

    return header


def _draw_rounded_card(
    base: Image.Image,
    content: Image.Image,
    x: int,
    y: int,
    padding: int = 12,
    radius: int = 16,
    shadow_offset: int = 4,
    shadow_blur: int = 8,
) -> None:
    """Draw a rounded card with shadow containing the content image.

    Args:
        base: Base image to draw on
        content: Content image to put in the card
        x: X position for the card
        y: Y position for the card
        padding: Padding inside the card
        radius: Corner radius
        shadow_offset: Shadow offset in pixels
        shadow_blur: Shadow blur amount (not used, simplified shadow)
    """
    card_width = content.width + 2 * padding
    card_height = content.height + 2 * padding

    # Create shadow (simple gray rectangle offset)
    shadow_color = "#d1d5db"  # Light gray shadow
    shadow = Image.new("RGBA", (card_width, card_height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle([0, 0, card_width - 1, card_height - 1], radius=radius, fill=shadow_color)
    base.paste(shadow, (x + shadow_offset, y + shadow_offset), shadow)

    # Create card background (white)
    card = Image.new("RGBA", (card_width, card_height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([0, 0, card_width - 1, card_height - 1], radius=radius, fill="#ffffff")
    base.paste(card, (x, y), card)

    # Paste content
    base.paste(content, (x + padding, y + padding))


def create_branded_og_image(
    plot_image: str | Path | Image.Image | bytes,
    output_path: str | Path | None = None,
    spec_id: str | None = None,
    library: str | None = None,
) -> Image.Image | bytes:
    """Create a branded OG image by adding pyplots.ai header to a plot.

    Design matches og-image.png style:
    - pyplots.ai logo at top
    - Tagline "Beautiful Python plotting made easy."
    - Plot in rounded paper card with shadow
    - spec_id · library label below

    Args:
        plot_image: Path to plot image, PIL Image, or bytes
        output_path: If provided, save to this path
        spec_id: Optional spec ID for subtitle
        library: Optional library name for subtitle

    Returns:
        PIL Image if output_path is None, otherwise bytes of PNG
    """
    # Load the plot image
    if isinstance(plot_image, bytes):
        img = Image.open(BytesIO(plot_image))
    elif isinstance(plot_image, Image.Image):
        img = plot_image
    else:
        img = Image.open(plot_image)

    # Convert to RGB if necessary
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Layout constants
    top_margin = 25
    logo_height = 55
    tagline_height = 35
    bottom_margin = 45
    card_padding = 12
    label_height = 30

    # Available space for the card
    header_total = top_margin + logo_height + tagline_height + 25  # More gap after tagline
    footer_total = label_height + bottom_margin
    available_height = OG_HEIGHT - header_total - footer_total - 2 * card_padding
    available_width = OG_WIDTH - 120  # 60px margin on each side

    # Scale plot to fit in available space
    scale = min(available_width / img.width, available_height / img.height)
    new_width = int(img.width * scale)
    new_height = int(img.height * scale)

    # Resize plot
    plot_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create final image
    final = Image.new("RGBA", (OG_WIDTH, OG_HEIGHT), PYPLOTS_BG)
    draw = ImageDraw.Draw(final)

    # Draw logo (centered at top)
    logo_font_size = 42
    logo_font = _get_font(logo_font_size)
    logo_text = "pyplots.ai"
    logo_bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
    logo_width = logo_bbox[2] - logo_bbox[0]
    logo_x = (OG_WIDTH - logo_width) // 2
    logo_y = top_margin
    _draw_pyplots_logo(draw, logo_x, logo_y, logo_font_size)

    # Draw tagline (matches website style - lowercase)
    tagline = "library-agnostic, ai-powered python plotting."
    tagline_font = _get_font(22, weight=400)
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (OG_WIDTH - tagline_width) // 2
    tagline_y = top_margin + logo_height + 18  # More space after logo
    draw.text((tagline_x, tagline_y), tagline, fill="#6b7280", font=tagline_font)

    # Draw card with plot
    card_x = (OG_WIDTH - new_width - 2 * card_padding) // 2
    card_y = header_total
    _draw_rounded_card(final, plot_resized, card_x, card_y, padding=card_padding)

    # Draw label below card
    if spec_id or library:
        label_parts = []
        if spec_id:
            label_parts.append(spec_id)
        if library:
            label_parts.append(library)
        label = " · ".join(label_parts)

        label_font = _get_font(20, weight=400)
        label_bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]
        label_x = (OG_WIDTH - label_width) // 2
        label_y = card_y + new_height + 2 * card_padding + 15
        draw = ImageDraw.Draw(final)  # Refresh draw after card paste
        draw.text((label_x, label_y), label, fill=PYPLOTS_DARK, font=label_font)

    # Convert to RGB for PNG output
    final_rgb = Image.new("RGB", final.size, PYPLOTS_BG)
    final_rgb.paste(final, mask=final.split()[3] if final.mode == "RGBA" else None)

    if output_path:
        final_rgb.save(output_path, "PNG", optimize=True)
        return final_rgb

    # Return as bytes
    buffer = BytesIO()
    final_rgb.save(buffer, "PNG", optimize=True)
    return buffer.getvalue()


def create_og_collage(
    images: list[str | Path | Image.Image | bytes],
    output_path: str | Path | None = None,
    spec_id: str | None = None,
    labels: list[str] | None = None,
) -> Image.Image | bytes:
    """Create a collage OG image from multiple plot images.

    Creates a 2x3 grid (2 rows, 3 columns) with pyplots.ai branding:
    - Large dominant logo and tagline at top
    - 6 plots in 16:9 rounded cards arranged in 2 rows
    - Labels below each card

    Args:
        images: List of plot images (paths, PIL Images, or bytes), up to 6
        output_path: If provided, save to this path
        spec_id: Optional spec ID for subtitle
        labels: Optional list of labels for each image (e.g., library names)

    Returns:
        PIL Image if output_path is None, otherwise bytes of PNG
    """
    if not images:
        raise ValueError("At least one image is required")

    # Load all images (max 6 for 2x3 grid)
    loaded_images: list[Image.Image] = []
    for img_input in images[:6]:
        if isinstance(img_input, bytes):
            img = Image.open(BytesIO(img_input))
        elif isinstance(img_input, Image.Image):
            img = img_input
        else:
            img = Image.open(img_input)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        loaded_images.append(img)

    # Create final image (RGBA for card transparency)
    final = Image.new("RGBA", (OG_WIDTH, OG_HEIGHT), PYPLOTS_BG)
    draw = ImageDraw.Draw(final)

    # Layout constants
    top_margin = 20
    side_margin = 40
    card_gap_x = 20  # Horizontal gap between cards
    card_gap_y = 8  # Vertical gap between rows
    card_padding = 6
    label_gap = 4  # Gap between card and label
    bottom_margin = 15

    # Draw logo (centered at top)
    logo_font_size = 38
    logo_font = _get_font(logo_font_size)
    logo_text = "pyplots.ai"
    logo_bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
    logo_width = logo_bbox[2] - logo_bbox[0]
    logo_x = (OG_WIDTH - logo_width) // 2
    logo_y = top_margin
    _draw_pyplots_logo(draw, logo_x, logo_y, logo_font_size)

    # Draw tagline (matches website style - lowercase)
    tagline = "library-agnostic, ai-powered python plotting."
    tagline_font = _get_font(18, weight=400)
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (OG_WIDTH - tagline_width) // 2
    tagline_y = top_margin + 58  # More space after logo
    draw.text((tagline_x, tagline_y), tagline, fill="#6b7280", font=tagline_font)

    # Grid layout: 2 rows x 3 columns
    cols = 3
    rows = 2

    # Label font and height
    label_font = _get_font(13, weight=400)
    label_height = 18

    # Calculate card area
    header_height = tagline_y + 35
    grid_top = header_height
    grid_bottom = OG_HEIGHT - bottom_margin

    # Available space for grid
    available_width = OG_WIDTH - 2 * side_margin - (cols - 1) * card_gap_x
    available_height = grid_bottom - grid_top - (rows - 1) * card_gap_y - rows * (label_height + label_gap)

    # Card slot dimensions
    slot_width = available_width // cols
    slot_height = available_height // rows

    # Card inner dimensions (16:9 aspect ratio)
    # Calculate max inner size that fits in slot while being 16:9
    inner_aspect = 16 / 9
    slot_inner_width = slot_width - 2 * card_padding
    slot_inner_height = slot_height - 2 * card_padding

    if slot_inner_width / slot_inner_height > inner_aspect:
        # Slot is wider than 16:9, constrain by height
        inner_height = slot_inner_height
        inner_width = int(inner_height * inner_aspect)
    else:
        # Slot is taller than 16:9, constrain by width
        inner_width = slot_inner_width
        inner_height = int(inner_width / inner_aspect)

    for i, img in enumerate(loaded_images):
        row = i // cols
        col = i % cols

        # Slot position
        slot_x = side_margin + col * (slot_width + card_gap_x)
        slot_y = grid_top + row * (slot_height + card_gap_y + label_height + label_gap)

        # Scale image to fit in 16:9 inner area
        scale = min(inner_width / img.width, inner_height / img.height)
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)

        # Resize image
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center card in slot
        actual_card_width = new_width + 2 * card_padding
        actual_card_height = new_height + 2 * card_padding
        card_x = slot_x + (slot_width - actual_card_width) // 2
        card_y = slot_y + (slot_height - actual_card_height) // 2

        # Draw card
        _draw_rounded_card(final, resized, card_x, card_y, padding=card_padding, radius=10, shadow_offset=2)

        # Add label below card
        if labels and i < len(labels):
            label = labels[i]
            draw = ImageDraw.Draw(final)
            bbox = draw.textbbox((0, 0), label, font=label_font)
            lbl_width = bbox[2] - bbox[0]
            label_x = slot_x + (slot_width - lbl_width) // 2
            label_y = card_y + actual_card_height + label_gap
            draw.text((label_x, label_y), label, fill=PYPLOTS_DARK, font=label_font)

    # Convert to RGB for PNG output
    final_rgb = Image.new("RGB", final.size, PYPLOTS_BG)
    final_rgb.paste(final, mask=final.split()[3] if final.mode == "RGBA" else None)

    if output_path:
        final_rgb.save(output_path, "PNG", optimize=True)
        return final_rgb

    # Return as bytes
    buffer = BytesIO()
    final_rgb.save(buffer, "PNG", optimize=True)
    return buffer.getvalue()


if __name__ == "__main__":
    import sys

    def print_usage() -> None:
        print("Usage:")
        print("  python -m core.images thumbnail <input> <output> [width]")
        print("  python -m core.images process <input> <output> [thumb]")
        print("  python -m core.images brand <input> <output> [spec_id] [library]")
        print("  python -m core.images collage <output> <img1> [img2] [img3] [img4]")
        print("")
        print("Examples:")
        print("  python -m core.images thumbnail plot.png thumb.png 400")
        print("  python -m core.images process plot.png out.png thumb.png")
        print("  python -m core.images brand plot.png og.png scatter-basic matplotlib")
        print("  python -m core.images collage og.png img1.png img2.png img3.png img4.png")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_usage()

    command = sys.argv[1]

    if command == "thumbnail":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        width = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
        w, h = create_thumbnail(input_file, output_file, width)
        print(f"Thumbnail: {w}x{h}px")

    elif command == "process":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        thumb_file = sys.argv[4] if len(sys.argv) > 4 else None
        res = process_plot_image(input_file, output_file, thumb_file)
        print(f"Processed: {res}")

    elif command == "brand":
        if len(sys.argv) < 4:
            print_usage()
        input_file, output_file = sys.argv[2], sys.argv[3]
        spec_id = sys.argv[4] if len(sys.argv) > 4 else None
        library = sys.argv[5] if len(sys.argv) > 5 else None
        create_branded_og_image(input_file, output_file, spec_id, library)
        print(f"Branded OG image: {output_file} ({OG_WIDTH}x{OG_HEIGHT}px)")

    elif command == "collage":
        if len(sys.argv) < 4:
            print_usage()
        output_file = sys.argv[2]
        input_files = sys.argv[3:]
        create_og_collage(input_files, output_file)
        print(f"Collage: {output_file} ({OG_WIDTH}x{OG_HEIGHT}px, {len(input_files)} images)")

    else:
        print(f"Unknown command: {command}")
        print_usage()
