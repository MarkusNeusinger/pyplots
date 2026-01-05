"""Utility functions for code processing."""

import re


def strip_noqa_comments(code: str | None) -> str | None:
    """Remove # noqa: comments from code for cleaner user display.

    Note:
        Uses regex-based matching, which will also remove noqa patterns inside
        string literals. This is acceptable for plot implementation code where
        noqa comments in strings are extremely rare.
    """
    if not code:
        return code
    return re.sub(r"\s*# noqa:[^\n]*", "", code)
