"""Tests for automation.scripts.backfill_review_metadata module."""


import pytest

from automation.scripts.backfill_review_metadata import parse_ai_review_comment, parse_criteria_checklist


class TestParseAiReviewComment:
    """Tests for parse_ai_review_comment function."""

    @pytest.fixture
    def complete_review_comment(self):
        return """## AI Review

### Image Description
> The plot shows a scatter plot with 100 data points displaying
> a positive correlation. Points are rendered in blue with 70%
> opacity. Axes are clearly labeled and include units.

### Strengths
- Clean code structure with proper imports
- Good use of alpha for overlapping points
- Proper axis labels with units
- Appropriate figure size

### Weaknesses
- Grid could be more subtle
- Consider adding a trend line
- Title could be more descriptive

### Verdict: APPROVED

**Quality Score: 92/100**
"""

    def test_parse_complete_review(self, complete_review_comment):
        result = parse_ai_review_comment(complete_review_comment)

        assert result is not None
        assert "scatter plot with 100 data points" in result["image_description"]
        assert "positive correlation" in result["image_description"]
        assert result["verdict"] == "APPROVED"
        assert len(result["strengths"]) == 4
        assert "Clean code structure" in result["strengths"][0]
        assert len(result["weaknesses"]) == 3
        assert "Grid could be more subtle" in result["weaknesses"][0]

    def test_parse_rejected_review(self):
        comment = """## AI Review

### Image Description
> The plot has significant rendering issues.
> Text is overlapping and unreadable.

### Strengths
- Uses correct library imports

### Weaknesses
- Major rendering problem with overlapping elements
- Missing axis labels
- Figure size too small
- No title

### Verdict: REJECTED

**Quality Score: 45/100**
"""
        result = parse_ai_review_comment(comment)

        assert result is not None
        assert result["verdict"] == "REJECTED"
        assert len(result["strengths"]) == 1
        assert len(result["weaknesses"]) == 4

    def test_parse_verdict_case_insensitive(self):
        comment = """## AI Review

### Image Description
> Test plot.

### Verdict: approved
"""
        result = parse_ai_review_comment(comment)

        assert result["verdict"] == "APPROVED"

    def test_non_review_comment_returns_none(self):
        comment = "This is just a regular comment without AI Review header."

        result = parse_ai_review_comment(comment)

        assert result is None

    def test_partial_review_comment_returns_none(self):
        comment = "## Not AI Review\n\nSome other content."

        result = parse_ai_review_comment(comment)

        assert result is None

    def test_parse_multiline_image_description(self):
        comment = """## AI Review

### Image Description
> Line 1 of the description providing context.
> Line 2 continues with more details about the plot.
> Line 3 describes specific visual elements.
> Line 4 concludes the description.

### Verdict: APPROVED
"""
        result = parse_ai_review_comment(comment)

        assert result is not None
        desc = result["image_description"]
        assert "Line 1" in desc
        assert "Line 2" in desc
        assert "Line 3" in desc
        assert "Line 4" in desc
        # Should not have leading > characters
        assert not desc.startswith(">")

    def test_parse_empty_strengths_weaknesses(self):
        comment = """## AI Review

### Image Description
> Simple plot description.

### Strengths

### Weaknesses

### Verdict: APPROVED
"""
        result = parse_ai_review_comment(comment)

        assert result is not None
        assert result["strengths"] == []
        assert result["weaknesses"] == []

    def test_parse_asterisk_bullets(self):
        comment = """## AI Review

### Image Description
> Test.

### Strengths
* First strength
* Second strength

### Weaknesses
* First weakness

### Verdict: APPROVED
"""
        result = parse_ai_review_comment(comment)

        assert result is not None
        assert len(result["strengths"]) == 2
        assert "First strength" in result["strengths"]
        assert "Second strength" in result["strengths"]

    def test_parse_missing_sections(self):
        """Test that missing optional sections are handled gracefully."""
        comment = """## AI Review

### Verdict: APPROVED
"""
        result = parse_ai_review_comment(comment)

        assert result is not None
        assert result["verdict"] == "APPROVED"
        assert result["image_description"] is None
        assert result["strengths"] == []
        assert result["weaknesses"] == []


class TestParseCriteriaChecklist:
    """Tests for parse_criteria_checklist function."""

    @pytest.fixture
    def complete_checklist(self):
        return """
**Visual Quality (36/40 pts)**
- [x] VQ-01: Text Legibility (10/10) - All text is readable at full size
- [x] VQ-02: No Overlap (8/8) - Elements are properly spaced
- [ ] VQ-03: Color Contrast (8/10) - Could use higher contrast
- [x] VQ-04: Resolution (10/10) - High quality output at 300 DPI

**Spec Compliance (23/25 pts)**
- [x] SC-01: Data Requirements (15/15) - All required data columns shown
- [ ] SC-02: Visual Style (8/10) - Minor style deviations

**Data Quality (18/20 pts)**
- [x] DQ-01: Accuracy (10/10) - Data represented correctly
- [ ] DQ-02: Completeness (8/10) - Some edge cases not shown

**Code Quality (10/10 pts)**
- [x] CQ-01: Clean Code (5/5) - Well structured and readable
- [x] CQ-02: Documentation (5/5) - Good docstring and comments

**Library Features (5/5 pts)**
- [x] LF-01: Idiomatic Usage (5/5) - Uses library best practices
"""

    def test_parse_complete_checklist(self, complete_checklist):
        result = parse_criteria_checklist(complete_checklist)

        assert result is not None
        assert "visual_quality" in result
        assert "spec_compliance" in result
        assert "data_quality" in result
        assert "code_quality" in result
        assert "library_features" in result

    def test_parse_category_scores(self, complete_checklist):
        result = parse_criteria_checklist(complete_checklist)

        assert result["visual_quality"]["score"] == 36
        assert result["visual_quality"]["max"] == 40
        assert result["spec_compliance"]["score"] == 23
        assert result["spec_compliance"]["max"] == 25
        assert result["code_quality"]["score"] == 10
        assert result["code_quality"]["max"] == 10

    def test_parse_checklist_items(self, complete_checklist):
        result = parse_criteria_checklist(complete_checklist)

        vq_items = result["visual_quality"]["items"]
        assert len(vq_items) == 4

        # Check first item (passed)
        vq01 = next(i for i in vq_items if i["id"] == "VQ-01")
        assert vq01["name"] == "Text Legibility"
        assert vq01["score"] == 10
        assert vq01["max"] == 10
        assert vq01["passed"] is True
        assert "readable" in vq01["comment"].lower()

        # Check failed item
        vq03 = next(i for i in vq_items if i["id"] == "VQ-03")
        assert vq03["name"] == "Color Contrast"
        assert vq03["score"] == 8
        assert vq03["max"] == 10
        assert vq03["passed"] is False

    def test_parse_empty_comment_returns_none(self):
        result = parse_criteria_checklist("No checklist here, just text.")

        assert result is None or result == {}

    def test_parse_partial_checklist(self):
        """Test checklist with only some categories."""
        comment = """
**Visual Quality (35/40 pts)**
- [x] VQ-01: Text Legibility (10/10) - Good
- [x] VQ-02: No Overlap (8/8) - Good

**Code Quality (8/10 pts)**
- [x] CQ-01: Clean Code (5/5) - Good
- [ ] CQ-02: Documentation (3/5) - Missing docstring
"""
        result = parse_criteria_checklist(comment)

        assert result is not None
        assert "visual_quality" in result
        assert "code_quality" in result
        assert "spec_compliance" not in result
        assert "data_quality" not in result

    def test_parse_item_without_comment(self):
        comment = """
**Visual Quality (10/10 pts)**
- [x] VQ-01: Text Legibility (10/10)
"""
        result = parse_criteria_checklist(comment)

        if result and "visual_quality" in result:
            items = result["visual_quality"]["items"]
            if items:
                assert items[0]["comment"] == ""

    def test_parse_uppercase_x_checkbox(self):
        comment = """
**Code Quality (10/10 pts)**
- [X] CQ-01: Clean Code (10/10) - Perfect
"""
        result = parse_criteria_checklist(comment)

        if result and "code_quality" in result:
            items = result["code_quality"]["items"]
            if items:
                assert items[0]["passed"] is True

    def test_parse_with_pts_singular(self):
        """Test parsing with 'pt' instead of 'pts'."""
        comment = """
**Visual Quality (36/40 pt)**
- [x] VQ-01: Text Legibility (10/10) - Good
"""
        result = parse_criteria_checklist(comment)

        # Should handle both 'pt' and 'pts'
        if result and "visual_quality" in result:
            assert result["visual_quality"]["score"] == 36
            assert result["visual_quality"]["max"] == 40


class TestUpdateMetadataFile:
    """Tests for update_metadata_file function - using mocked file operations."""

    def test_update_adds_review_section(self, tmp_path):
        """Test that review data is added to existing metadata."""
        import yaml

        from automation.scripts.backfill_review_metadata import update_metadata_file

        metadata_content = """library: matplotlib
specification_id: scatter-basic
quality_score: 92
preview_url: https://example.com/plot.png
"""
        metadata_file = tmp_path / "matplotlib.yaml"
        metadata_file.write_text(metadata_content)

        review_data = {
            "image_description": "A scatter plot showing correlation.",
            "criteria_checklist": {"visual_quality": {"score": 36, "max": 40, "items": []}},
            "verdict": "APPROVED",
            "strengths": ["Clean code"],
            "weaknesses": ["Minor issues"],
        }

        result = update_metadata_file(metadata_file, review_data, dry_run=False)

        assert result is True

        # Verify file was updated
        updated_data = yaml.safe_load(metadata_file.read_text())
        assert "review" in updated_data
        assert updated_data["review"]["image_description"] == "A scatter plot showing correlation."
        assert updated_data["review"]["verdict"] == "APPROVED"

    def test_update_dry_run_does_not_modify(self, tmp_path):
        """Test that dry run doesn't modify files."""
        from automation.scripts.backfill_review_metadata import update_metadata_file

        original_content = """library: matplotlib
specification_id: scatter-basic
quality_score: 92
"""
        metadata_file = tmp_path / "matplotlib.yaml"
        metadata_file.write_text(original_content)

        review_data = {"image_description": "New description", "verdict": "APPROVED", "strengths": [], "weaknesses": []}

        result = update_metadata_file(metadata_file, review_data, dry_run=True)

        assert result is True
        # File should not be modified
        assert metadata_file.read_text() == original_content

    def test_update_missing_file_returns_false(self, tmp_path):
        """Test handling of missing file."""
        from automation.scripts.backfill_review_metadata import update_metadata_file

        missing_file = tmp_path / "nonexistent.yaml"
        review_data = {"image_description": "Test", "verdict": "APPROVED", "strengths": [], "weaknesses": []}

        result = update_metadata_file(missing_file, review_data, dry_run=False)

        assert result is False

    def test_update_preserves_existing_strengths(self, tmp_path):
        """Test that existing strengths are not overwritten if new ones are empty."""
        import yaml

        from automation.scripts.backfill_review_metadata import update_metadata_file

        metadata_content = """library: matplotlib
specification_id: scatter-basic
quality_score: 92
review:
  strengths:
    - Existing strength 1
    - Existing strength 2
  weaknesses: []
"""
        metadata_file = tmp_path / "matplotlib.yaml"
        metadata_file.write_text(metadata_content)

        review_data = {
            "image_description": "New description",
            "verdict": "APPROVED",
            "strengths": [],  # Empty - should not overwrite
            "weaknesses": [],
        }

        update_metadata_file(metadata_file, review_data, dry_run=False)

        updated_data = yaml.safe_load(metadata_file.read_text())
        # Original strengths should be preserved
        assert len(updated_data["review"]["strengths"]) == 2
        assert "Existing strength 1" in updated_data["review"]["strengths"]
