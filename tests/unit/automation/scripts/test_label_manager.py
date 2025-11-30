"""Tests for automation.scripts.label_manager module."""

from automation.scripts.label_manager import (
    LabelChange,
    build_gh_issue_edit_command,
    build_gh_pr_edit_command,
    get_attempt_label,
    get_current_status,
    get_library_label,
    get_quality_label,
    get_quality_transition,
    get_status_transition,
    is_approved,
    is_rejected,
)


class TestLabelChange:
    """Tests for LabelChange dataclass."""

    def test_to_gh_args_add_and_remove(self):
        change = LabelChange(add=["testing"], remove=["generating"])
        args = change.to_gh_args()
        assert '--remove-label "generating"' in args
        assert '--add-label "testing"' in args

    def test_to_gh_args_only_add(self):
        change = LabelChange(add=["testing", "library:matplotlib"], remove=[])
        args = change.to_gh_args()
        assert '--add-label "testing"' in args
        assert '--add-label "library:matplotlib"' in args
        assert "--remove-label" not in args

    def test_to_gh_args_only_remove(self):
        change = LabelChange(add=[], remove=["generating"])
        args = change.to_gh_args()
        assert '--remove-label "generating"' in args
        assert "--add-label" not in args

    def test_is_empty(self):
        assert LabelChange(add=[], remove=[]).is_empty() is True
        assert LabelChange(add=["test"], remove=[]).is_empty() is False
        assert LabelChange(add=[], remove=["test"]).is_empty() is False


class TestGetStatusTransition:
    """Tests for get_status_transition function."""

    def test_simple_transition(self):
        change = get_status_transition(["generating", "library:matplotlib"], "testing")
        assert change.add == ["testing"]
        assert change.remove == ["generating"]

    def test_removes_multiple_status_labels(self):
        # Edge case: multiple status labels present (shouldn't happen, but handle it)
        change = get_status_transition(["generating", "reviewing"], "testing")
        assert "testing" in change.add
        assert "generating" in change.remove
        assert "reviewing" in change.remove

    def test_no_change_if_already_in_status(self):
        change = get_status_transition(["testing", "library:matplotlib"], "testing")
        assert change.add == []
        assert change.remove == []

    def test_preserves_non_status_labels(self):
        change = get_status_transition(["generating", "library:matplotlib", "ai-attempt-1"], "testing")
        assert "library:matplotlib" not in change.remove
        assert "ai-attempt-1" not in change.remove


class TestGetQualityLabel:
    """Tests for get_quality_label function."""

    def test_excellent_score(self):
        assert get_quality_label(90) == "quality:excellent"
        assert get_quality_label(95) == "quality:excellent"
        assert get_quality_label(100) == "quality:excellent"

    def test_good_score(self):
        assert get_quality_label(85) == "quality:good"
        assert get_quality_label(89) == "quality:good"

    def test_needs_work_score(self):
        assert get_quality_label(75) == "quality:needs-work"
        assert get_quality_label(84) == "quality:needs-work"

    def test_poor_score(self):
        assert get_quality_label(74) == "quality:poor"
        assert get_quality_label(50) == "quality:poor"
        assert get_quality_label(0) == "quality:poor"


class TestGetQualityTransition:
    """Tests for get_quality_transition function."""

    def test_adds_new_quality_label(self):
        change = get_quality_transition(["library:matplotlib"], 90)
        assert "quality:excellent" in change.add
        assert change.remove == []

    def test_replaces_existing_quality_label(self):
        change = get_quality_transition(["quality:poor", "library:matplotlib"], 90)
        assert "quality:excellent" in change.add
        assert "quality:poor" in change.remove

    def test_no_change_if_same_quality(self):
        change = get_quality_transition(["quality:excellent"], 95)
        assert change.add == []
        assert change.remove == []


class TestGetAttemptLabel:
    """Tests for get_attempt_label function."""

    def test_valid_attempts(self):
        assert get_attempt_label(1) == "ai-attempt-1"
        assert get_attempt_label(2) == "ai-attempt-2"
        assert get_attempt_label(3) == "ai-attempt-3"

    def test_invalid_attempts(self):
        assert get_attempt_label(0) is None
        assert get_attempt_label(4) is None
        assert get_attempt_label(-1) is None


class TestGetLibraryLabel:
    """Tests for get_library_label function."""

    def test_lowercase(self):
        assert get_library_label("matplotlib") == "library:matplotlib"

    def test_converts_to_lowercase(self):
        assert get_library_label("MATPLOTLIB") == "library:matplotlib"
        assert get_library_label("Seaborn") == "library:seaborn"


class TestApprovalChecks:
    """Tests for is_approved and is_rejected functions."""

    def test_is_approved(self):
        assert is_approved(["ai-approved", "library:matplotlib"]) is True
        assert is_approved(["reviewing", "library:matplotlib"]) is False
        assert is_approved([]) is False

    def test_is_rejected(self):
        assert is_rejected(["ai-rejected", "library:matplotlib"]) is True
        assert is_rejected(["reviewing", "library:matplotlib"]) is False
        assert is_rejected([]) is False


class TestGetCurrentStatus:
    """Tests for get_current_status function."""

    def test_finds_status(self):
        assert get_current_status(["generating", "library:matplotlib"]) == "generating"
        assert get_current_status(["testing"]) == "testing"
        assert get_current_status(["ai-approved", "quality:excellent"]) == "ai-approved"

    def test_no_status(self):
        assert get_current_status(["library:matplotlib"]) is None
        assert get_current_status([]) is None


class TestBuildGhCommands:
    """Tests for gh command building functions."""

    def test_build_gh_issue_edit_command(self):
        change = LabelChange(add=["testing"], remove=["generating"])
        cmd = build_gh_issue_edit_command(42, change)
        assert cmd == 'gh issue edit 42 --remove-label "generating" --add-label "testing"'

    def test_build_gh_pr_edit_command(self):
        change = LabelChange(add=["testing"], remove=["generating"])
        cmd = build_gh_pr_edit_command(123, change)
        assert cmd == 'gh pr edit 123 --remove-label "generating" --add-label "testing"'

    def test_empty_change_returns_empty_string(self):
        change = LabelChange(add=[], remove=[])
        assert build_gh_issue_edit_command(42, change) == ""
        assert build_gh_pr_edit_command(42, change) == ""
