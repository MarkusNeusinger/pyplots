"""
Tests for AI prompts structure and content validation.

Best practices for prompt testing:
1. File existence - All expected prompts exist
2. Required sections - Core sections are present (## Role, ## Task, etc.)
3. No placeholders - No TODO, FIXME, or {placeholder} left behind
4. Cross-references valid - Referenced files exist
5. Consistent formatting - Markdown is well-formed
"""

import re
from pathlib import Path

import pytest


# Base paths
PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "prompts"
LIBRARY_PROMPTS_DIR = PROMPTS_DIR / "library"

# Expected files
EXPECTED_BASE_PROMPTS = [
    "plot-generator.md",
    "quality-criteria.md",
    "quality-evaluator.md",
    "auto-tagger.md",
    "spec-validator.md",
    "spec-id-generator.md",
]

EXPECTED_LIBRARY_PROMPTS = [
    "matplotlib.md",
    "seaborn.md",
    "plotly.md",
    "bokeh.md",
    "altair.md",
    "plotnine.md",
    "pygal.md",
    "highcharts.md",
]


class TestPromptFileExistence:
    """Test that all expected prompt files exist."""

    def test_prompts_directory_exists(self) -> None:
        """Prompts directory should exist."""
        assert PROMPTS_DIR.exists(), f"Prompts directory not found: {PROMPTS_DIR}"
        assert PROMPTS_DIR.is_dir(), f"Prompts path is not a directory: {PROMPTS_DIR}"

    def test_library_directory_exists(self) -> None:
        """Library prompts subdirectory should exist."""
        assert LIBRARY_PROMPTS_DIR.exists(), f"Library prompts not found: {LIBRARY_PROMPTS_DIR}"
        assert LIBRARY_PROMPTS_DIR.is_dir()

    @pytest.mark.parametrize("filename", EXPECTED_BASE_PROMPTS)
    def test_base_prompt_exists(self, filename: str) -> None:
        """Each base prompt file should exist."""
        filepath = PROMPTS_DIR / filename
        assert filepath.exists(), f"Missing base prompt: {filename}"

    @pytest.mark.parametrize("filename", EXPECTED_LIBRARY_PROMPTS)
    def test_library_prompt_exists(self, filename: str) -> None:
        """Each library-specific prompt file should exist."""
        filepath = LIBRARY_PROMPTS_DIR / filename
        assert filepath.exists(), f"Missing library prompt: {filename}"


class TestPromptStructure:
    """Test prompt structure and required sections."""

    @pytest.fixture
    def plot_generator_content(self) -> str:
        """Load plot-generator.md content."""
        return (PROMPTS_DIR / "plot-generator.md").read_text()

    @pytest.fixture
    def quality_criteria_content(self) -> str:
        """Load quality-criteria.md content."""
        return (PROMPTS_DIR / "quality-criteria.md").read_text()

    def test_plot_generator_has_required_sections(self, plot_generator_content: str) -> None:
        """Plot generator should have Role, Task, Rules sections."""
        required_sections = ["## Role", "## Task", "## Rules", "## Output"]
        for section in required_sections:
            assert section in plot_generator_content, f"Missing section: {section}"

    def test_plot_generator_has_code_template(self, plot_generator_content: str) -> None:
        """Plot generator should include a code template."""
        assert "```python" in plot_generator_content, "Missing Python code template"
        assert "def create_plot" in plot_generator_content, "Missing create_plot function template"

    def test_quality_criteria_has_scoring_section(self, quality_criteria_content: str) -> None:
        """Quality criteria should have scoring information."""
        assert "## Scoring" in quality_criteria_content
        assert "85" in quality_criteria_content, "Pass threshold (85) not mentioned"

    def test_quality_criteria_has_visual_and_code_quality(self, quality_criteria_content: str) -> None:
        """Quality criteria should cover both visual and code quality."""
        assert "## Visual Quality" in quality_criteria_content
        assert "## Code Quality" in quality_criteria_content

    @pytest.mark.parametrize("filename", EXPECTED_LIBRARY_PROMPTS)
    def test_library_prompt_has_required_sections(self, filename: str) -> None:
        """Each library prompt should have import, create figure, and save sections."""
        content = (LIBRARY_PROMPTS_DIR / filename).read_text()
        library_name = filename.replace(".md", "")

        # Check for header
        assert f"# {library_name}" in content.lower(), f"Missing header for {library_name}"

        # Check for import section
        assert "## Import" in content or "import" in content.lower(), f"Missing import section in {filename}"

        # Check for code examples
        assert "```python" in content, f"Missing Python code examples in {filename}"

    @pytest.mark.parametrize("filename", EXPECTED_LIBRARY_PROMPTS)
    def test_library_prompt_has_return_type(self, filename: str) -> None:
        """Each library prompt should specify return type."""
        content = (LIBRARY_PROMPTS_DIR / filename).read_text()
        # Either explicit return type section or type hint in code
        has_return_type = "## Return Type" in content or "-> " in content
        assert has_return_type, f"Missing return type specification in {filename}"


class TestNoPlaceholders:
    """Test that no placeholder text is left in prompts."""

    PLACEHOLDER_PATTERNS = [
        r"\{TODO\}",
        r"\bTODO\b",
        r"\bFIXME\b",
        r"\bXXX\b",
        r"\{placeholder\}",
        r"\{PLACEHOLDER\}",
        r"<INSERT.*>",
        r"\[TBD\]",
    ]

    def _get_all_prompt_files(self) -> list[Path]:
        """Get all markdown files in prompts directory."""
        files = list(PROMPTS_DIR.glob("*.md"))
        files.extend(LIBRARY_PROMPTS_DIR.glob("*.md"))
        return files

    @pytest.mark.parametrize("pattern", PLACEHOLDER_PATTERNS, ids=[p.replace("\\", "") for p in PLACEHOLDER_PATTERNS])
    def test_no_placeholder_pattern(self, pattern: str) -> None:
        """No placeholder patterns should exist in any prompt."""
        regex = re.compile(pattern, re.IGNORECASE)

        for filepath in self._get_all_prompt_files():
            content = filepath.read_text()
            matches = regex.findall(content)
            assert not matches, f"Found placeholder '{pattern}' in {filepath.name}: {matches}"

    def test_no_empty_sections(self) -> None:
        """No empty sections (## Header followed by another ## or end of file)."""
        empty_section_pattern = re.compile(r"^## .+\n\s*(?=^## |\Z)", re.MULTILINE)

        for filepath in self._get_all_prompt_files():
            content = filepath.read_text()
            matches = empty_section_pattern.findall(content)
            # Filter out intentionally minimal sections
            real_empty = [m for m in matches if len(m.strip()) < 20]
            assert not real_empty, f"Found empty sections in {filepath.name}: {real_empty}"


class TestCrossReferences:
    """Test that cross-references in prompts are valid."""

    def test_plot_generator_references_exist(self) -> None:
        """Files referenced in plot-generator.md should exist."""
        content = (PROMPTS_DIR / "plot-generator.md").read_text()

        # Check for references to library prompts
        if "prompts/library/" in content:
            # All library prompts should exist
            for lib_file in EXPECTED_LIBRARY_PROMPTS:
                assert (LIBRARY_PROMPTS_DIR / lib_file).exists()

    def test_no_broken_internal_links(self) -> None:
        """Internal markdown links should point to existing files."""
        link_pattern = re.compile(r"\[.*?\]\((?!http)([^)]+\.md)\)")

        for filepath in PROMPTS_DIR.glob("**/*.md"):
            content = filepath.read_text()
            links = link_pattern.findall(content)

            for link in links:
                # Resolve relative to the file's directory
                target = (filepath.parent / link).resolve()
                # Also check relative to prompts root
                target_alt = (PROMPTS_DIR / link).resolve()

                exists = target.exists() or target_alt.exists()
                assert exists, f"Broken link in {filepath.name}: {link}"


class TestPromptConsistency:
    """Test consistency across prompts."""

    def test_all_libraries_have_same_structure(self) -> None:
        """All library prompts should have consistent structure."""
        structures: dict[str, set[str]] = {}
        section_pattern = re.compile(r"^## (.+)$", re.MULTILINE)

        for lib_file in EXPECTED_LIBRARY_PROMPTS:
            content = (LIBRARY_PROMPTS_DIR / lib_file).read_text()
            sections = set(section_pattern.findall(content))
            structures[lib_file] = sections

        # Check that all have at least the common sections
        common_sections = {"Import"}  # Minimal common section
        for lib_file, sections in structures.items():
            missing = common_sections - sections
            assert not missing, f"{lib_file} missing common sections: {missing}"

    def test_quality_score_threshold_consistent(self) -> None:
        """Quality threshold (85) should be consistent across prompts."""
        files_to_check = [
            PROMPTS_DIR / "plot-generator.md",
            PROMPTS_DIR / "quality-criteria.md",
            PROMPTS_DIR / "quality-evaluator.md",
        ]

        for filepath in files_to_check:
            if filepath.exists():
                content = filepath.read_text()
                # If file mentions scoring, it should use 85 as threshold
                if "score" in content.lower() and "threshold" in content.lower():
                    assert "85" in content, f"Inconsistent threshold in {filepath.name}"


class TestPromptQuality:
    """Test overall prompt quality."""

    def test_prompts_not_too_short(self) -> None:
        """Prompts should have substantial content (>100 chars)."""
        min_length = 100

        for filepath in PROMPTS_DIR.glob("**/*.md"):
            if filepath.name == "README.md":
                continue
            content = filepath.read_text()
            assert len(content) > min_length, f"{filepath.name} too short ({len(content)} chars)"

    def test_prompts_have_headers(self) -> None:
        """All prompts should have at least one header."""
        for filepath in PROMPTS_DIR.glob("**/*.md"):
            if filepath.name == "README.md":
                continue
            content = filepath.read_text()
            assert re.search(r"^#+ ", content, re.MULTILINE), f"{filepath.name} has no markdown headers"

    def test_code_blocks_have_language(self) -> None:
        """Code blocks should specify language for syntax highlighting."""
        # Pattern for code blocks without language
        unlabeled_pattern = re.compile(r"^```\s*$", re.MULTILINE)
        labeled_pattern = re.compile(r"^```\w+", re.MULTILINE)

        for filepath in PROMPTS_DIR.glob("**/*.md"):
            content = filepath.read_text()
            unlabeled = len(unlabeled_pattern.findall(content))
            labeled = len(labeled_pattern.findall(content))

            # If there are code blocks, at least some should have language hints
            # Prompts often use unlabeled blocks for output examples
            total = unlabeled + labeled
            if total > 0:
                labeled_ratio = labeled / total
                assert labeled_ratio >= 0.2, (
                    f"{filepath.name} has too few labeled code blocks "
                    f"({labeled}/{total} = {labeled_ratio:.0%}, need ≥20%)"
                )
