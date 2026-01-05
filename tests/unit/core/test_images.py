"""Tests for core.images module."""

from pathlib import Path

import pytest
from PIL import Image

from core.images import create_thumbnail, optimize_png, process_plot_image


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

    def test_default_width(self, sample_image: Path, tmp_path: Path) -> None:
        """Should use default width of 1200 if not specified."""
        output_path = tmp_path / "thumb.png"
        width, height = create_thumbnail(sample_image, output_path)

        assert width == 1200  # Default width is 1200
        assert height == 900  # Original 800x600 scaled to 1200x900 (4:3 ratio)

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


class TestProcessPlotImage:
    """Tests for process_plot_image function."""

    def test_creates_optimized_image_and_thumbnail(self, sample_image: Path, tmp_path: Path) -> None:
        """Should create both optimized image and thumbnail."""
        output_path = tmp_path / "output.png"
        thumb_path = tmp_path / "thumb.png"

        result = process_plot_image(sample_image, output_path, thumb_path)

        assert output_path.exists()
        assert thumb_path.exists()
        assert result["output"] == str(output_path)
        assert result["thumbnail"] == str(thumb_path)
        assert result["thumb_size"][0] == 1200  # Default width is 1200
        assert result["thumb_size"][1] == 900  # Original 800x600 scaled to 1200x900

    def test_without_thumbnail(self, sample_image: Path, tmp_path: Path) -> None:
        """Should work without creating a thumbnail."""
        output_path = tmp_path / "output.png"

        result = process_plot_image(sample_image, output_path, thumb_path=None)

        assert output_path.exists()
        assert "thumbnail" not in result

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


class TestErrorCases:
    """Tests for error handling."""

    def test_thumbnail_file_not_found(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for missing input."""
        with pytest.raises(FileNotFoundError):
            create_thumbnail(tmp_path / "nonexistent.png", tmp_path / "out.png")

    def test_optimize_file_not_found(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for missing input."""
        with pytest.raises(FileNotFoundError):
            optimize_png(tmp_path / "nonexistent.png", tmp_path / "out.png")


class TestPngquantFallback:
    """Tests for pngquant fallback behavior."""

    def test_pillow_fallback_when_no_pngquant(self, sample_image: Path, tmp_path: Path) -> None:
        """Should use Pillow fallback when pngquant is not available."""
        import core.images

        # Save original value
        original_has_pngquant = core.images._HAS_PNGQUANT
        try:
            # Mock pngquant not being available
            core.images._HAS_PNGQUANT = False

            output_path = tmp_path / "optimized.png"
            bytes_saved = optimize_png(sample_image, output_path)

            assert output_path.exists()
            assert isinstance(bytes_saved, int)
        finally:
            # Restore original value
            core.images._HAS_PNGQUANT = original_has_pngquant

    def test_optimize_png_with_pillow_fallback_inplace(self, tmp_path: Path) -> None:
        """Should optimize in-place with Pillow fallback."""
        import core.images

        # Create a test image
        img_path = tmp_path / "to_optimize.png"
        img = Image.new("RGB", (800, 600), color=(100, 150, 200))
        img.save(img_path)

        original_has_pngquant = core.images._HAS_PNGQUANT
        try:
            core.images._HAS_PNGQUANT = False
            bytes_saved = optimize_png(img_path, output_path=None)
            assert img_path.exists()
            assert isinstance(bytes_saved, int)
        finally:
            core.images._HAS_PNGQUANT = original_has_pngquant


class TestImageFormats:
    """Tests for different image formats and edge cases."""

    def test_rgba_image(self, tmp_path: Path) -> None:
        """Should handle RGBA images with transparency."""
        img_path = tmp_path / "rgba.png"
        img = Image.new("RGBA", (400, 300), color=(100, 150, 200, 128))
        img.save(img_path)

        output_path = tmp_path / "processed.png"
        process_plot_image(img_path, output_path)

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


class TestCLI:
    """Tests for command-line interface."""

    def test_cli_thumbnail_command(self, sample_image: Path, tmp_path: Path, monkeypatch, capsys) -> None:
        """Should run thumbnail command from CLI."""
        import sys

        output_path = tmp_path / "thumb.png"

        # Mock sys.argv for CLI
        monkeypatch.setattr(sys, "argv", ["images", "thumbnail", str(sample_image), str(output_path), "300"])

        # Run the module
        import runpy

        try:
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)
        except SystemExit:
            pass  # Expected if print_usage was called

        # Check output was created
        assert output_path.exists()
        captured = capsys.readouterr()
        assert "300x" in captured.out  # Should print dimensions

    def test_cli_thumbnail_default_width(self, sample_image: Path, tmp_path: Path, monkeypatch, capsys) -> None:
        """Should use default width of 1200 for thumbnail."""
        import sys

        output_path = tmp_path / "thumb.png"

        monkeypatch.setattr(sys, "argv", ["images", "thumbnail", str(sample_image), str(output_path)])

        import runpy

        try:
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)
        except SystemExit:
            pass

        assert output_path.exists()
        result_img = Image.open(output_path)
        assert result_img.width == 1200

    def test_cli_process_command(self, sample_image: Path, tmp_path: Path, monkeypatch, capsys) -> None:
        """Should run process command from CLI."""
        import sys

        output_path = tmp_path / "output.png"
        thumb_path = tmp_path / "thumb.png"

        monkeypatch.setattr(sys, "argv", ["images", "process", str(sample_image), str(output_path), str(thumb_path)])

        import runpy

        try:
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)
        except SystemExit:
            pass

        assert output_path.exists()
        assert thumb_path.exists()
        captured = capsys.readouterr()
        assert "Processed:" in captured.out

    def test_cli_process_without_thumbnail(self, sample_image: Path, tmp_path: Path, monkeypatch, capsys) -> None:
        """Should run process command without thumbnail."""
        import sys

        output_path = tmp_path / "output.png"

        monkeypatch.setattr(sys, "argv", ["images", "process", str(sample_image), str(output_path)])

        import runpy

        try:
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)
        except SystemExit:
            pass

        assert output_path.exists()
        captured = capsys.readouterr()
        assert "Processed:" in captured.out

    def test_cli_unknown_command(self, monkeypatch, capsys) -> None:
        """Should print usage for unknown command."""
        import sys

        monkeypatch.setattr(sys, "argv", ["images", "unknown"])

        import runpy

        with pytest.raises(SystemExit):
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)

        captured = capsys.readouterr()
        assert "Unknown command: unknown" in captured.out

    def test_cli_no_args(self, monkeypatch, capsys) -> None:
        """Should print usage when no arguments given."""
        import sys

        monkeypatch.setattr(sys, "argv", ["images"])

        import runpy

        with pytest.raises(SystemExit):
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_cli_thumbnail_missing_args(self, monkeypatch, capsys) -> None:
        """Should print usage when thumbnail args are missing."""
        import sys

        monkeypatch.setattr(sys, "argv", ["images", "thumbnail", "input.png"])

        import runpy

        with pytest.raises(SystemExit):
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_cli_process_missing_args(self, monkeypatch, capsys) -> None:
        """Should print usage when process args are missing."""
        import sys

        monkeypatch.setattr(sys, "argv", ["images", "process", "input.png"])

        import runpy

        with pytest.raises(SystemExit):
            runpy.run_module("core.images", run_name="__main__", alter_sys=True)

        captured = capsys.readouterr()
        assert "Usage:" in captured.out
