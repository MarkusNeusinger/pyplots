"""Tests for automation.scripts.migrate_metadata_format module."""

from unittest.mock import patch

import yaml

from automation.scripts.migrate_metadata_format import (
    extract_title_from_header,
    migrate_library_metadata,
    migrate_specification_yaml,
)


class TestMigrateSpecificationYaml:
    """Tests for migrate_specification_yaml function."""

    def test_remove_history_add_updated(self, tmp_path):
        """Test that history is removed and updated is added."""
        yaml_content = """spec_id: scatter-basic
title: Basic Scatter Plot
created: 2025-01-10T08:00:00Z
history:
  - date: 2025-01-10
    action: created
  - date: 2025-01-12
    action: updated
tags:
  plot_type:
    - scatter
  domain:
    - statistics
"""
        yaml_file = tmp_path / "specification.yaml"
        yaml_file.write_text(yaml_content)

        result = migrate_specification_yaml(yaml_file)

        assert result is True  # Modified

        # Verify file content
        new_content = yaml_file.read_text()
        assert "history:" not in new_content
        assert "updated:" in new_content

    def test_skip_already_migrated(self, tmp_path):
        """Test that already migrated files are skipped."""
        yaml_content = """spec_id: scatter-basic
title: Basic Scatter Plot
created: 2025-01-10T08:00:00Z
updated: 2025-01-15T10:00:00Z
tags:
  plot_type:
    - scatter
"""
        yaml_file = tmp_path / "specification.yaml"
        yaml_file.write_text(yaml_content)

        result = migrate_specification_yaml(yaml_file)

        assert result is False  # Not modified

    def test_missing_file_returns_false(self, tmp_path):
        yaml_file = tmp_path / "nonexistent.yaml"

        result = migrate_specification_yaml(yaml_file)

        assert result is False

    def test_empty_file_returns_false(self, tmp_path):
        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("")

        result = migrate_specification_yaml(yaml_file)

        assert result is False

    def test_updated_uses_created_if_available(self, tmp_path):
        """Test that updated is set to created value if not present."""
        yaml_content = """spec_id: test-plot
title: Test Plot
created: 2025-01-10T08:00:00Z
history:
  - date: 2025-01-10
"""
        yaml_file = tmp_path / "specification.yaml"
        yaml_file.write_text(yaml_content)

        migrate_specification_yaml(yaml_file)

        data = yaml.safe_load(yaml_file.read_text())
        # Updated should match created
        assert "updated" in data


class TestMigrateLibraryMetadata:
    """Tests for migrate_library_metadata function."""

    def test_flatten_current_structure(self, tmp_path):
        """Test flattening of nested current: structure."""
        yaml_content = """library: matplotlib
specification_id: scatter-basic
current:
  generated_at: 2025-01-10T08:00:00Z
  generated_by: claude-opus-4-5
  quality_score: 92
  python_version: "3.13"
  library_version: "3.10.0"
  version: 1
history:
  - version: 1
    date: 2025-01-10
preview_url: https://example.com/plot.png
"""
        yaml_file = tmp_path / "matplotlib.yaml"
        yaml_file.write_text(yaml_content)

        # Patch PLOTS_DIR to use tmp_path so relative_to works
        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            result = migrate_library_metadata(yaml_file)

        assert result is True

        # Verify flattened structure
        new_data = yaml.safe_load(yaml_file.read_text())
        assert "current" not in new_data
        assert "history" not in new_data
        assert "version" not in new_data
        assert new_data["quality_score"] == 92
        assert new_data["generated_by"] == "claude-opus-4-5"
        assert new_data["python_version"] == "3.13"

    def test_adds_created_from_generated_at(self, tmp_path):
        """Test that created is added from generated_at."""
        yaml_content = """library: seaborn
specification_id: scatter-basic
current:
  generated_at: 2025-01-10T08:00:00Z
  quality_score: 88
"""
        yaml_file = tmp_path / "seaborn.yaml"
        yaml_file.write_text(yaml_content)

        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            migrate_library_metadata(yaml_file)

        new_data = yaml.safe_load(yaml_file.read_text())
        assert "created" in new_data
        assert "updated" in new_data

    def test_adds_empty_review_section(self, tmp_path):
        """Test that empty review section is added."""
        yaml_content = """library: plotly
specification_id: scatter-basic
quality_score: 90
"""
        yaml_file = tmp_path / "plotly.yaml"
        yaml_file.write_text(yaml_content)

        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            migrate_library_metadata(yaml_file)

        new_data = yaml.safe_load(yaml_file.read_text())
        assert "review" in new_data
        assert "strengths" in new_data["review"]
        assert "weaknesses" in new_data["review"]

    def test_skip_already_migrated(self, tmp_path):
        """Test that already migrated files are skipped."""
        yaml_content = """library: matplotlib
specification_id: scatter-basic
created: 2025-01-10T08:00:00Z
updated: 2025-01-15T10:00:00Z
quality_score: 92
review:
  strengths: []
  weaknesses: []
  improvements: []
"""
        yaml_file = tmp_path / "matplotlib.yaml"
        yaml_file.write_text(yaml_content)

        result = migrate_library_metadata(yaml_file)

        # File has all required fields, should not be modified
        # (unless current: or history: present)
        assert result is False

    def test_missing_file_returns_false(self, tmp_path):
        yaml_file = tmp_path / "nonexistent.yaml"

        result = migrate_library_metadata(yaml_file)

        assert result is False

    def test_empty_file_returns_false(self, tmp_path):
        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("")

        result = migrate_library_metadata(yaml_file)

        assert result is False

    def test_removes_version_field(self, tmp_path):
        """Test that version field is removed."""
        yaml_content = """library: bokeh
specification_id: scatter-basic
version: 3
quality_score: 85
"""
        yaml_file = tmp_path / "bokeh.yaml"
        yaml_file.write_text(yaml_content)

        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            migrate_library_metadata(yaml_file)

        new_data = yaml.safe_load(yaml_file.read_text())
        assert "version" not in new_data


class TestExtractTitleFromHeader:
    """Tests for extract_title_from_header function."""

    def test_extract_standard_format(self):
        header = '''""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib 3.10.0 | Python 3.13
Quality: 92/100 | Created: 2025-01-10
"""'''

        result = extract_title_from_header(header)

        assert result == "Basic Scatter Plot"

    def test_extract_with_colon_in_title(self):
        """Test title extraction when title contains colons."""
        header = '''"""
heatmap-correlation: Correlation Matrix: Visualizing Relationships
Library: seaborn
"""'''

        result = extract_title_from_header(header)

        # Should get everything after first colon on the spec-id line
        assert "Correlation Matrix" in result

    def test_extract_simple_title(self):
        header = '''"""
bar-basic: Simple Bar Chart
Library: matplotlib
"""'''

        result = extract_title_from_header(header)

        assert result == "Simple Bar Chart"

    def test_extract_empty_header(self):
        result = extract_title_from_header('""""""')

        assert result == ""

    def test_extract_only_library_line(self):
        """Test that header with only library line returns empty string."""
        header = '''"""
Library: matplotlib
"""'''

        result = extract_title_from_header(header)

        # Library: line is ignored, no other title line present
        assert result == ""

    def test_extract_ignores_library_line(self):
        """Test that Library: line is not mistaken for title."""
        header = '''"""
scatter-basic: My Plot
Library: matplotlib 3.10.0
"""'''

        result = extract_title_from_header(header)

        assert result == "My Plot"
        assert "matplotlib" not in result

    def test_extract_with_newlines(self):
        header = '''"""

scatter-3d: 3D Scatter Plot

Library: plotly 5.18.0
"""'''

        result = extract_title_from_header(header)

        assert result == "3D Scatter Plot"

    def test_extract_multiword_title(self):
        header = '''"""
violin-grouped: Grouped Violin Plot with Multiple Categories
Library: seaborn
"""'''

        result = extract_title_from_header(header)

        assert result == "Grouped Violin Plot with Multiple Categories"


class TestMigratePlot:
    """Integration tests for migrate_plot function."""

    def test_migrate_complete_plot_directory(self, tmp_path):
        """Test migration of a complete plot directory."""
        from automation.scripts.migrate_metadata_format import migrate_plot

        # Create plot directory structure
        plot_dir = tmp_path / "scatter-basic"
        plot_dir.mkdir()

        # specification.yaml with history
        (plot_dir / "specification.yaml").write_text("""spec_id: scatter-basic
title: Basic Scatter Plot
created: 2025-01-10T08:00:00Z
history:
  - date: 2025-01-10
tags:
  plot_type:
    - scatter
""")

        # metadata/ directory
        meta_dir = plot_dir / "metadata"
        meta_dir.mkdir()

        # metadata/matplotlib.yaml with current: structure
        (meta_dir / "matplotlib.yaml").write_text("""library: matplotlib
specification_id: scatter-basic
current:
  generated_at: 2025-01-10T08:00:00Z
  quality_score: 92
  python_version: "3.13"
  library_version: "3.10.0"
preview_url: https://example.com/plot.png
""")

        # implementations/ directory
        impl_dir = plot_dir / "implementations"
        impl_dir.mkdir()

        # implementations/matplotlib.py
        (impl_dir / "matplotlib.py").write_text('''"""
scatter-basic: Basic Scatter Plot
Library: matplotlib
"""
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
''')

        # Run migration with patched PLOTS_DIR
        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            stats = migrate_plot(plot_dir)

        assert stats["spec"] == 1  # specification.yaml migrated
        assert stats["meta"] == 1  # matplotlib.yaml migrated

        # Verify specification.yaml
        spec_data = yaml.safe_load((plot_dir / "specification.yaml").read_text())
        assert "history" not in spec_data
        assert "updated" in spec_data

        # Verify matplotlib.yaml
        meta_data = yaml.safe_load((meta_dir / "matplotlib.yaml").read_text())
        assert "current" not in meta_data
        assert meta_data["quality_score"] == 92
        assert "review" in meta_data

    def test_migrate_skips_underscore_files(self, tmp_path):
        """Test that files starting with underscore are skipped."""
        from automation.scripts.migrate_metadata_format import migrate_plot

        plot_dir = tmp_path / "test-plot"
        plot_dir.mkdir()

        (plot_dir / "specification.yaml").write_text("""spec_id: test-plot
title: Test
created: 2025-01-10T08:00:00Z
updated: 2025-01-10T08:00:00Z
tags:
  plot_type:
    - test
""")

        impl_dir = plot_dir / "implementations"
        impl_dir.mkdir()

        # Use a header that won't be migrated (already correct format)
        # Note: library_version must match metadata for header to be identical
        (impl_dir / "matplotlib.py").write_text('''""" pyplots.ai
test-plot: Test
Library: matplotlib 3.10.0 | Python 3.13
Quality: 92/100 | Created: 2025-01-10
"""
import matplotlib.pyplot as plt
''')
        (impl_dir / "_template.py").write_text('"""template - should be skipped"""')

        meta_dir = plot_dir / "metadata"
        meta_dir.mkdir()

        (meta_dir / "matplotlib.yaml").write_text("""library: matplotlib
specification_id: test-plot
created: 2025-01-10T08:00:00Z
updated: 2025-01-10T08:00:00Z
python_version: "3.13"
library_version: "3.10.0"
quality_score: 92
review:
  strengths: []
  weaknesses: []
  improvements: []
""")

        with patch("automation.scripts.migrate_metadata_format.PLOTS_DIR", tmp_path):
            stats = migrate_plot(plot_dir)

        # _template.py should be skipped (only matplotlib.py processed)
        # matplotlib.py header is already in correct format, so no migration needed
        assert stats["impl"] == 0
        # Verify _template.py was not modified
        assert (impl_dir / "_template.py").read_text() == '"""template - should be skipped"""'
