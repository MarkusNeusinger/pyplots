"""Utility functions for code processing."""

import re


def strip_noqa_comments(code: str | None) -> str | None:
    """Remove # noqa: comments from code for cleaner user display."""
    if not code:
        return code
    return re.sub(r"\s*# noqa:[^\n]*", "", code)
