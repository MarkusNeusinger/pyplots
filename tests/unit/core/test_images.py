"""Tests for core.images module."""

from pathlib import Path

import pytest
from PIL import Image

from core.images import add_watermark, create_thumbnail, optimize_png, process_plot_image


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a sample test image."""
    img_path = tmp_path / "test_image.png"
    img = Image.new("RGB", (800, 600), color=(100, 150, 200))
    img.save(img_path)
    return img_path


class TestCreateThumbnail:
    """Tests for create_thumbnail function."""

    def test_creates_thumbnail_with_correct_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Thumbnail should have the specified width."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(sample_image, output_path, width=400)

        assert width == 400
        assert output_path.exists()

        # Verify the actual image dimensions
        result_img = Image.open(output_path)
        assert result_img.width == 400

    def test_maintains_aspect_ratio(self, sample_image: Path, tmp_path: Path) -> None:
        """Thumbnail should maintain the original aspect ratio."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(sample_image, output_path, width=400)

        # Original is 800x600 (4:3), so 400 width should give 300 height
        assert height == 300

        result_img = Image.open(output_path)
        assert result_img.height == 300

    def test_custom_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Thumbnail should respect custom width parameter."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(sample_image, output_path, width=200)

        assert width == 200
        assert height == 150  # Maintains 4:3 ratio

    def test_handles_path_objects(self, sample_image: Path, tmp_path: Path) -> None:
        """Function should accept Path objects."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(Path(sample_image), Path(output_path), width=400)

        assert width == 400
        assert output_path.exists()


class TestAddWatermark:
    """Tests for add_watermark function."""

    def test_adds_watermark_to_image(self, sample_image: Path, tmp_path: Path) -> None:
        """Watermark should be added to the image."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, text="pyplots.ai")

        assert output_path.exists()

        # Verify the image was created and has same dimensions
        result_img = Image.open(output_path)
        original_img = Image.open(sample_image)
        assert result_img.size == original_img.size

    def test_custom_watermark_text(self, sample_image: Path, tmp_path: Path) -> None:
        """Function should accept custom watermark text."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, text="Custom Watermark")

        assert output_path.exists()

    def test_custom_opacity(self, sample_image: Path, tmp_path: Path) -> None:
        """Function should accept custom opacity."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, opacity=0.5)

        assert output_path.exists()


class TestProcessPlotImage:
    """Tests for process_plot_image function."""

    def test_creates_watermarked_image_and_thumbnail(self, sample_image: Path, tmp_path: Path) -> None:
        """Should create both watermarked image and thumbnail."""
        output_path = tmp_path / "output.png"
        thumb_path = tmp_path / "thumb.png"

        result = process_plot_image(sample_image, output_path, thumb_path, watermark_text="pyplots.ai")

        assert output_path.exists()
        assert thumb_path.exists()
        assert result["output"] == str(output_path)
        assert result["thumbnail"] == str(thumb_path)
        assert result["thumb_size"] == (600, 450)

    def test_without_thumbnail(self, sample_image: Path, tmp_path: Path) -> None:
        """Should work without creating a thumbnail."""
        output_path = tmp_path / "output.png"

        result = process_plot_image(sample_image, output_path, thumb_path=None)

        assert output_path.exists()
        assert "thumbnail" not in result

    def test_without_watermark(self, sample_image: Path, tmp_path: Path) -> None:
        """Should work without adding watermark."""
        output_path = tmp_path / "output.png"
        thumb_path = tmp_path / "thumb.png"

        process_plot_image(sample_image, output_path, thumb_path, add_watermark_flag=False)

        assert output_path.exists()
        assert thumb_path.exists()

    def test_with_spec_id(self, sample_image: Path, tmp_path: Path) -> None:
        """Should add spec_id to bottom-left corner."""
        output_path = tmp_path / "output.png"

        result = process_plot_image(sample_image, output_path, spec_id="histogram-basic", add_watermark_flag=True)

        assert output_path.exists()
        assert result["output"] == str(output_path)

    def test_without_optimization(self, sample_image: Path, tmp_path: Path) -> None:
        """Should work without PNG optimization."""
        output_path = tmp_path / "output.png"

        result = process_plot_image(sample_image, output_path, optimize=False)

        assert output_path.exists()
        assert "bytes_saved" not in result

    def test_custom_thumb_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Should respect custom thumbnail width."""
        output_path = tmp_path / "output.png"
        thumb_path = tmp_path / "thumb.png"

        result = process_plot_image(sample_image, output_path, thumb_path, thumb_width=300)

        assert result["thumb_size"][0] == 300


class TestOptimizePng:
    """Tests for optimize_png function."""

    def test_optimizes_image(self, sample_image: Path, tmp_path: Path) -> None:
        """Should optimize PNG file."""
        output_path = tmp_path / "optimized.png"
        bytes_saved = optimize_png(sample_image, output_path)

        assert output_path.exists()
        # bytes_saved can be negative if optimized is larger (rare for simple images)
        assert isinstance(bytes_saved, int)

    def test_overwrites_input_when_no_output(self, tmp_path: Path) -> None:
        """Should overwrite input file when output_path is None."""
        # Create a larger image for better optimization potential
        img_path = tmp_path / "to_optimize.png"
        img = Image.new("RGB", (1000, 1000), color=(100, 150, 200))
        img.save(img_path)

        bytes_saved = optimize_png(img_path, output_path=None)

        # File should still exist and function should return bytes saved
        assert img_path.exists()
        assert isinstance(bytes_saved, int)

    def test_accepts_path_objects(self, sample_image: Path, tmp_path: Path) -> None:
        """Should accept Path objects."""
        output_path = tmp_path / "optimized.png"
        bytes_saved = optimize_png(Path(sample_image), Path(output_path))

        assert output_path.exists()
        assert isinstance(bytes_saved, int)

    def test_accepts_string_paths(self, sample_image: Path, tmp_path: Path) -> None:
        """Should accept string paths."""
        output_path = tmp_path / "optimized.png"
        optimize_png(str(sample_image), str(output_path))

        assert output_path.exists()


class TestAddWatermarkExtended:
    """Extended tests for add_watermark function."""

    def test_with_spec_id(self, sample_image: Path, tmp_path: Path) -> None:
        """Should add spec_id to bottom-left corner."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, spec_id="scatter-basic")

        assert output_path.exists()

    def test_custom_font_size(self, sample_image: Path, tmp_path: Path) -> None:
        """Should accept custom font size."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, font_size=30)

        assert output_path.exists()

    def test_custom_padding(self, sample_image: Path, tmp_path: Path) -> None:
        """Should accept custom padding."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(sample_image, output_path, padding=20)

        assert output_path.exists()

    def test_all_custom_params(self, sample_image: Path, tmp_path: Path) -> None:
        """Should accept all custom parameters together."""
        output_path = tmp_path / "watermarked.png"
        add_watermark(
            sample_image, output_path, text="Custom Text", spec_id="my-spec", opacity=0.8, font_size=18, padding=15
        )

        assert output_path.exists()


class TestCreateThumbnailExtended:
    """Extended tests for create_thumbnail function."""

    def test_default_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Should use default width of 600 if not specified."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(sample_image, output_path)

        assert width == 600
        assert height == 450  # 800x600 -> 600x450 (4:3 ratio)

    def test_portrait_image(self, tmp_path: Path) -> None:
        """Should handle portrait orientation images."""
        # Create portrait image (600x800)
        img_path = tmp_path / "portrait.png"
        img = Image.new("RGB", (600, 800), color=(100, 150, 200))
        img.save(img_path)

        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(img_path, output_path, width=300)

        assert width == 300
        assert height == 400  # Maintains 3:4 ratio

    def test_square_image(self, tmp_path: Path) -> None:
        """Should handle square images."""
        # Create square image
        img_path = tmp_path / "square.png"
        img = Image.new("RGB", (500, 500), color=(100, 150, 200))
        img.save(img_path)

        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(img_path, output_path, width=250)

        assert width == 250
        assert height == 250

    def test_very_small_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Should handle very small thumbnail widths."""
        output_path = tmp_path / "tiny.png"
        width, height = create_thumbnail(sample_image, output_path, width=50)

        assert width == 50
        result_img = Image.open(output_path)
        assert result_img.width == 50


class TestErrorCases:
    """Tests for error handling."""

    def test_thumbnail_file_not_found(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for missing input."""
        with pytest.raises(FileNotFoundError):
            create_thumbnail(tmp_path / "nonexistent.png", tmp_path / "out.png")

    def test_watermark_file_not_found(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for missing input."""
        with pytest.raises(FileNotFoundError):
            add_watermark(tmp_path / "nonexistent.png", tmp_path / "out.png")

    def test_optimize_file_not_found(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for missing input."""
        with pytest.raises(FileNotFoundError):
            optimize_png(tmp_path / "nonexistent.png", tmp_path / "out.png")


class TestImageFormats:
    """Tests for different image formats and edge cases."""

    def test_rgba_image(self, tmp_path: Path) -> None:
        """Should handle RGBA images with transparency."""
        img_path = tmp_path / "rgba.png"
        img = Image.new("RGBA", (400, 300), color=(100, 150, 200, 128))
        img.save(img_path)

        output_path = tmp_path / "watermarked.png"
        add_watermark(img_path, output_path)

        assert output_path.exists()

    def test_grayscale_image(self, tmp_path: Path) -> None:
        """Should handle grayscale images."""
        img_path = tmp_path / "gray.png"
        img = Image.new("L", (400, 300), color=128)
        img.save(img_path)

        # Thumbnail should work
        thumb_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(img_path, thumb_path, width=200)

        assert thumb_path.exists()
        assert width == 200

    def test_large_image(self, tmp_path: Path) -> None:
        """Should handle large images."""
        img_path = tmp_path / "large.png"
        img = Image.new("RGB", (4000, 3000), color=(100, 150, 200))
        img.save(img_path)

        thumb_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(img_path, thumb_path, width=400)

        assert width == 400
        assert height == 300  # Maintains 4:3 ratio
