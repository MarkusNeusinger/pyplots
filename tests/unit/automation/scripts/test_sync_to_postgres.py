"""Tests for automation.scripts.sync_to_postgres module."""

from datetime import datetime

from automation.scripts.sync_to_postgres import (
    convert_datetimes_to_strings,
    parse_bullet_points,
    parse_library_metadata_yaml,
    parse_metadata_yaml,
    parse_spec_markdown,
    parse_timestamp,
    scan_plot_directory,
)


class TestParseTimestamp:
    """Tests for parse_timestamp function."""

    def test_parse_datetime_object(self):
        dt = datetime(2025, 1, 10, 8, 0, 0)
        result = parse_timestamp(dt)
        assert result == dt
        assert result.tzinfo is None

    def test_parse_datetime_with_timezone(self):
        from datetime import timezone

        dt = datetime(2025, 1, 10, 8, 0, 0, tzinfo=timezone.utc)
        result = parse_timestamp(dt)
        assert result == datetime(2025, 1, 10, 8, 0, 0)
        assert result.tzinfo is None

    def test_parse_iso_string_with_z(self):
        result = parse_timestamp("2025-01-10T08:00:00Z")
        assert result == datetime(2025, 1, 10, 8, 0, 0)

    def test_parse_iso_string_with_offset(self):
        result = parse_timestamp("2025-01-10T08:00:00+00:00")
        assert result == datetime(2025, 1, 10, 8, 0, 0)

    def test_parse_invalid_string(self):
        result = parse_timestamp("not-a-date")
        assert result is None

    def test_parse_none(self):
        result = parse_timestamp(None)
        assert result is None

    def test_parse_integer_returns_none(self):
        result = parse_timestamp(12345)
        assert result is None


class TestParseBulletPoints:
    """Tests for parse_bullet_points function."""

    def test_parse_dash_bullets(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        result = parse_bullet_points(text)
        assert result == ["Item 1", "Item 2", "Item 3"]

    def test_parse_asterisk_bullets(self):
        text = "* Item 1\n* Item 2"
        result = parse_bullet_points(text)
        assert result == ["Item 1", "Item 2"]

    def test_parse_mixed_bullets(self):
        text = "- Item 1\n* Item 2\n- Item 3"
        result = parse_bullet_points(text)
        assert result == ["Item 1", "Item 2", "Item 3"]

    def test_parse_with_leading_whitespace(self):
        text = "  - Item 1\n  - Item 2"
        result = parse_bullet_points(text)
        assert result == ["Item 1", "Item 2"]

    def test_parse_empty_string(self):
        result = parse_bullet_points("")
        assert result == []

    def test_parse_no_bullets(self):
        text = "Just some text\nwithout bullets"
        result = parse_bullet_points(text)
        assert result == []

    def test_parse_bullets_with_extra_spaces(self):
        text = "-   Item with spaces  \n-  Another item"
        result = parse_bullet_points(text)
        assert result == ["Item with spaces", "Another item"]


class TestConvertDatetimesToStrings:
    """Tests for convert_datetimes_to_strings function."""

    def test_convert_datetime(self):
        dt = datetime(2025, 1, 10, 8, 0, 0)
        result = convert_datetimes_to_strings(dt)
        assert result == "2025-01-10T08:00:00"

    def test_convert_string_unchanged(self):
        result = convert_datetimes_to_strings("test string")
        assert result == "test string"

    def test_convert_integer_unchanged(self):
        result = convert_datetimes_to_strings(42)
        assert result == 42

    def test_convert_nested_dict(self):
        dt = datetime(2025, 1, 10, 8, 0, 0)
        data = {"created": dt, "nested": {"updated": dt}, "name": "test"}
        result = convert_datetimes_to_strings(data)
        assert result["created"] == "2025-01-10T08:00:00"
        assert result["nested"]["updated"] == "2025-01-10T08:00:00"
        assert result["name"] == "test"

    def test_convert_list(self):
        dt = datetime(2025, 1, 10, 8, 0, 0)
        result = convert_datetimes_to_strings([dt, "string", 123])
        assert result == ["2025-01-10T08:00:00", "string", 123]

    def test_convert_empty_dict(self):
        result = convert_datetimes_to_strings({})
        assert result == {}

    def test_convert_empty_list(self):
        result = convert_datetimes_to_strings([])
        assert result == []


class TestParseSpecMarkdown:
    """Tests for parse_spec_markdown function."""

    def test_parse_complete_spec(self, tmp_path):
        spec_content = """# scatter-basic: Basic Scatter Plot

## Description
A simple scatter plot showing the relationship between two variables.

## Applications
- Correlation analysis
- Data exploration
- Trend identification

## Data
- X values (numeric)
- Y values (numeric)

## Notes
- Use alpha for overlapping points
- Consider adding a trend line
"""
        spec_dir = tmp_path / "scatter-basic"
        spec_dir.mkdir()
        spec_file = spec_dir / "specification.md"
        spec_file.write_text(spec_content)

        result = parse_spec_markdown(spec_file)

        assert result["id"] == "scatter-basic"
        assert result["title"] == "Basic Scatter Plot"
        assert "relationship between two variables" in result["description"]
        assert result["applications"] == ["Correlation analysis", "Data exploration", "Trend identification"]
        assert len(result["data"]) == 2
        assert result["notes"] == ["Use alpha for overlapping points", "Consider adding a trend line"]

    def test_parse_spec_without_notes(self, tmp_path):
        spec_content = """# bar-basic: Basic Bar Chart

## Description
A simple bar chart for comparing categories.

## Applications
- Category comparison

## Data
- Categories
- Values
"""
        spec_dir = tmp_path / "bar-basic"
        spec_dir.mkdir()
        spec_file = spec_dir / "specification.md"
        spec_file.write_text(spec_content)

        result = parse_spec_markdown(spec_file)

        assert result["id"] == "bar-basic"
        assert result["title"] == "Basic Bar Chart"
        assert result["notes"] == []

    def test_parse_spec_without_title_match(self, tmp_path):
        spec_content = """# Just a Title Without Colon

## Description
Some description.

## Applications
- One application

## Data
- Some data
"""
        spec_dir = tmp_path / "no-colon-title"
        spec_dir.mkdir()
        spec_file = spec_dir / "specification.md"
        spec_file.write_text(spec_content)

        result = parse_spec_markdown(spec_file)

        # Falls back to directory name
        assert result["id"] == "no-colon-title"
        assert result["title"] == "no-colon-title"

    def test_parse_spec_minimal_sections(self, tmp_path):
        """Test parsing spec with minimal content in sections."""
        spec_content = """# minimal-spec: Minimal Spec

## Description
Minimal description.

## Applications
- One app

## Data
- One data point
"""
        spec_dir = tmp_path / "minimal-spec"
        spec_dir.mkdir()
        spec_file = spec_dir / "specification.md"
        spec_file.write_text(spec_content)

        result = parse_spec_markdown(spec_file)

        assert result["id"] == "minimal-spec"
        assert result["description"] == "Minimal description."
        assert result["applications"] == ["One app"]
        assert result["data"] == ["One data point"]


class TestParseMetadataYaml:
    """Tests for parse_metadata_yaml function."""

    def test_parse_valid_spec_yaml(self, tmp_path):
        yaml_content = """spec_id: scatter-basic
title: Basic Scatter Plot
created: 2025-01-10T08:00:00Z
tags:
  plot_type: [scatter]
  domain: [statistics]
"""
        yaml_file = tmp_path / "specification.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_metadata_yaml(yaml_file)

        assert result is not None
        assert result["spec_id"] == "scatter-basic"
        assert result["title"] == "Basic Scatter Plot"
        assert result["tags"]["plot_type"] == ["scatter"]

    def test_parse_with_specification_id(self, tmp_path):
        """Test backwards compatibility with specification_id key."""
        yaml_content = """specification_id: scatter-basic
title: Basic Scatter Plot
"""
        yaml_file = tmp_path / "spec.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_metadata_yaml(yaml_file)

        assert result is not None
        assert result["specification_id"] == "scatter-basic"

    def test_parse_missing_spec_id_returns_none(self, tmp_path):
        yaml_content = """title: No Spec ID
tags:
  plot_type: [scatter]
"""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_metadata_yaml(yaml_file)

        assert result is None

    def test_parse_empty_file_returns_none(self, tmp_path):
        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("")

        result = parse_metadata_yaml(yaml_file)

        assert result is None

    def test_parse_invalid_yaml_returns_none(self, tmp_path):
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("not: valid: yaml: : here")

        result = parse_metadata_yaml(yaml_file)

        assert result is None


class TestParseLibraryMetadataYaml:
    """Tests for parse_library_metadata_yaml function."""

    def test_parse_valid_library_metadata(self, tmp_path):
        yaml_content = """library: matplotlib
specification_id: scatter-basic
quality_score: 92
preview_url: https://storage.example.com/plot.png
python_version: "3.13"
library_version: "3.10.0"
"""
        yaml_file = tmp_path / "matplotlib.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_library_metadata_yaml(yaml_file)

        assert result is not None
        assert result["library"] == "matplotlib"
        assert result["quality_score"] == 92
        assert result["python_version"] == "3.13"

    def test_parse_missing_library_returns_none(self, tmp_path):
        yaml_content = """specification_id: scatter-basic
quality_score: 92
"""
        yaml_file = tmp_path / "no_library.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_library_metadata_yaml(yaml_file)

        assert result is None

    def test_parse_with_review_section(self, tmp_path):
        yaml_content = """library: seaborn
specification_id: scatter-basic
quality_score: 88
review:
  strengths:
    - Clean code
    - Good colors
  weaknesses:
    - Missing grid
"""
        yaml_file = tmp_path / "seaborn.yaml"
        yaml_file.write_text(yaml_content)

        result = parse_library_metadata_yaml(yaml_file)

        assert result is not None
        assert result["review"]["strengths"] == ["Clean code", "Good colors"]
        assert result["review"]["weaknesses"] == ["Missing grid"]


class TestScanPlotDirectory:
    """Tests for scan_plot_directory function."""

    def test_scan_complete_directory(self, tmp_path):
        # Create complete plot directory structure
        plot_dir = tmp_path / "scatter-basic"
        plot_dir.mkdir()

        # specification.md
        (plot_dir / "specification.md").write_text("""# scatter-basic: Basic Scatter Plot

## Description
A simple scatter plot.

## Applications
- Correlation analysis

## Data
- X values
- Y values
""")

        # specification.yaml
        (plot_dir / "specification.yaml").write_text("""spec_id: scatter-basic
title: Basic Scatter Plot
created: 2025-01-10T08:00:00Z
issue: 42
suggested: testuser
tags:
  plot_type: [scatter]
  domain: [statistics]
""")

        # implementations/
        impl_dir = plot_dir / "implementations"
        impl_dir.mkdir()
        (impl_dir / "matplotlib.py").write_text('''"""pyplots.ai"""
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.savefig("plot.png")
''')

        # metadata/
        meta_dir = plot_dir / "metadata"
        meta_dir.mkdir()
        (meta_dir / "matplotlib.yaml").write_text("""library: matplotlib
specification_id: scatter-basic
quality_score: 92
preview_url: https://storage.example.com/plot.png
python_version: "3.13"
library_version: "3.10.0"
review:
  strengths:
    - Clean code
  weaknesses: []
""")

        result = scan_plot_directory(plot_dir)

        assert result is not None
        assert result["spec"]["id"] == "scatter-basic"
        assert result["spec"]["title"] == "Basic Scatter Plot"
        assert result["spec"]["issue"] == 42
        assert result["spec"]["suggested"] == "testuser"
        assert len(result["implementations"]) == 1

        impl = result["implementations"][0]
        assert impl["spec_id"] == "scatter-basic"
        assert impl["library_id"] == "matplotlib"
        assert impl["quality_score"] == 92
        assert impl["python_version"] == "3.13"
        assert impl["review_strengths"] == ["Clean code"]

    def test_scan_missing_spec_returns_none(self, tmp_path):
        plot_dir = tmp_path / "empty-plot"
        plot_dir.mkdir()

        result = scan_plot_directory(plot_dir)

        assert result is None

    def test_scan_legacy_spec_md(self, tmp_path):
        """Test scanning with legacy spec.md filename."""
        plot_dir = tmp_path / "legacy-plot"
        plot_dir.mkdir()

        # Use legacy filename
        (plot_dir / "spec.md").write_text("""# legacy-plot: Legacy Plot

## Description
A legacy format plot.

## Applications
- Testing

## Data
- Values
""")

        result = scan_plot_directory(plot_dir)

        assert result is not None
        assert result["spec"]["id"] == "legacy-plot"
        assert result["spec"]["title"] == "Legacy Plot"

    def test_scan_skips_underscore_files(self, tmp_path):
        """Test that files starting with underscore are skipped."""
        plot_dir = tmp_path / "test-plot"
        plot_dir.mkdir()

        (plot_dir / "specification.md").write_text("""# test-plot: Test

## Description
Test plot.

## Applications
- Testing

## Data
- Values
""")

        impl_dir = plot_dir / "implementations"
        impl_dir.mkdir()
        (impl_dir / "matplotlib.py").write_text("# matplotlib")
        (impl_dir / "_template.py").write_text("# template - should be skipped")

        result = scan_plot_directory(plot_dir)

        assert result is not None
        assert len(result["implementations"]) == 1
        assert result["implementations"][0]["library_id"] == "matplotlib"

    def test_scan_without_implementations(self, tmp_path):
        """Test scanning a plot with only specification, no implementations."""
        plot_dir = tmp_path / "spec-only"
        plot_dir.mkdir()

        (plot_dir / "specification.md").write_text("""# spec-only: Spec Only

## Description
A specification without implementations.

## Applications
- Future work

## Data
- TBD
""")

        (plot_dir / "specification.yaml").write_text("""spec_id: spec-only
title: Spec Only
created: 2025-01-10T08:00:00Z
tags:
  plot_type: [scatter]
""")

        result = scan_plot_directory(plot_dir)

        assert result is not None
        assert result["spec"]["id"] == "spec-only"
        assert result["implementations"] == []

    def test_scan_with_legacy_nested_current(self, tmp_path):
        """Test scanning with legacy current: nested structure in metadata."""
        plot_dir = tmp_path / "legacy-nested"
        plot_dir.mkdir()

        (plot_dir / "specification.md").write_text("""# legacy-nested: Legacy Nested

## Description
Test.

## Applications
- Test

## Data
- Test
""")

        impl_dir = plot_dir / "implementations"
        impl_dir.mkdir()
        (impl_dir / "matplotlib.py").write_text("# code")

        meta_dir = plot_dir / "metadata"
        meta_dir.mkdir()
        (meta_dir / "matplotlib.yaml").write_text("""library: matplotlib
specification_id: legacy-nested
current:
  generated_at: 2025-01-10T08:00:00Z
  quality_score: 85
  python_version: "3.12"
""")

        result = scan_plot_directory(plot_dir)

        assert result is not None
        impl = result["implementations"][0]
        assert impl["quality_score"] == 85
        assert impl["python_version"] == "3.12"
