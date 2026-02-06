"""Workflow state management for composable agentic workflows.

Provides persistent state management via file storage and
transient state passing between scripts via stdin/stdout.
"""

import json
import os
import sys
from typing import Any, Dict, Optional


class WorkflowState:
    """Persistent state container for multi-phase workflows.

    State is stored in agentic/runs/{run_id}/state.json and can be
    passed between scripts via stdin/stdout (JSON piping).

    Usage:
        # Create new state
        state = WorkflowState(run_id="abc12345", prompt="fix the bug")

        # Update fields
        state.update(task_type="bug", plan_file="agentic/specs/bug-abc12345-fix-api.md")

        # Save to disk
        state.save(working_dir="/path/to/project")

        # Load existing state
        state = WorkflowState.load("abc12345", working_dir="/path/to/project")

        # Pipe between scripts
        state.to_stdout()  # in plan.py
        state = WorkflowState.from_stdin()  # in build.py
    """

    STATE_FILENAME = "state.json"

    # Core fields that are persisted
    CORE_FIELDS = {
        "run_id", "prompt", "task_type", "plan_file", "classify_reason",
        "test_passed", "test_failed_count", "review_success", "review_blocker_count",
    }

    def __init__(self, run_id: str, prompt: str = ""):
        if not run_id:
            raise ValueError("run_id is required for WorkflowState")
        self.data: Dict[str, Any] = {"run_id": run_id, "prompt": prompt}

    def update(self, **kwargs) -> None:
        """Update state with new key-value pairs (only core fields)."""
        for key, value in kwargs.items():
            if key in self.CORE_FIELDS:
                self.data[key] = value

    def get(self, key: str, default=None):
        """Get value from state by key."""
        return self.data.get(key, default)

    @property
    def run_id(self) -> str:
        return self.data["run_id"]

    @property
    def prompt(self) -> str:
        return self.data.get("prompt", "")

    @property
    def task_type(self) -> Optional[str]:
        return self.data.get("task_type")

    @property
    def plan_file(self) -> Optional[str]:
        return self.data.get("plan_file")

    @property
    def test_passed(self) -> Optional[bool]:
        return self.data.get("test_passed")

    @property
    def test_failed_count(self) -> Optional[int]:
        return self.data.get("test_failed_count")

    @property
    def review_success(self) -> Optional[bool]:
        return self.data.get("review_success")

    @property
    def review_blocker_count(self) -> Optional[int]:
        return self.data.get("review_blocker_count")

    def _get_state_path(self, working_dir: str) -> str:
        """Get path to state file."""
        return os.path.join(working_dir, "agentic", "runs", self.run_id, self.STATE_FILENAME)

    def save(self, working_dir: str, phase: Optional[str] = None) -> str:
        """Save state to agentic/runs/{run_id}/state.json.

        Returns:
            Path to the saved state file.
        """
        state_path = self._get_state_path(working_dir)
        os.makedirs(os.path.dirname(state_path), exist_ok=True)

        with open(state_path, "w") as f:
            json.dump(self.data, f, indent=2)

        return state_path

    @classmethod
    def load(cls, run_id: str, working_dir: str) -> Optional["WorkflowState"]:
        """Load state from file if it exists.

        Returns:
            WorkflowState instance or None if not found.
        """
        state_path = os.path.join(working_dir, "agentic", "runs", run_id, cls.STATE_FILENAME)

        if not os.path.exists(state_path):
            return None

        try:
            with open(state_path, "r") as f:
                data = json.load(f)

            state = cls(run_id=data["run_id"], prompt=data.get("prompt", ""))
            state.data = data
            return state
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading state from {state_path}: {e}", file=sys.stderr)
            return None

    @classmethod
    def from_stdin(cls) -> Optional["WorkflowState"]:
        """Read state from stdin (for piped input from plan.py).

        Returns:
            WorkflowState instance or None if no piped input.
        """
        if sys.stdin.isatty():
            return None
        try:
            input_data = sys.stdin.read()
            if not input_data.strip():
                return None
            data = json.loads(input_data)
            run_id = data.get("run_id")
            if not run_id:
                return None
            state = cls(run_id=run_id, prompt=data.get("prompt", ""))
            state.data = data
            return state
        except (json.JSONDecodeError, EOFError):
            return None

    def to_stdout(self) -> None:
        """Write state to stdout as JSON (for piping to build.py)."""
        print(json.dumps(self.data, indent=2))
