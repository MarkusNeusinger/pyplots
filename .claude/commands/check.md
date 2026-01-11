# Quick Code Check

> Fast code quality check for recent changes. Use `/refactor` for comprehensive analysis.

## Run Checks

```bash
# Lint check
uv run ruff check .

# Format check
uv run ruff format . --check && echo "Formatting OK" || echo "Formatting issues found"

# Quick unit tests
uv run pytest tests/unit -x -q --tb=short 2>/dev/null | tail -30
```

## Check Recent Changes

```bash
# Files changed vs main
git diff --name-only main... 2>/dev/null || git diff --name-only HEAD~5
```

## Summary

Provide a brief summary:
1. Any lint/format issues found
2. Test status
3. Quick recommendations for the changed files
