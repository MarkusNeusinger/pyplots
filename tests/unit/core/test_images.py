"""Tests for core.images module."""

from pathlib import Path

import pytest
from PIL import Image

from core.images import add_watermark, create_thumbnail, process_plot_image


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
