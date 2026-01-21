# Task Completion Checklist

## Before Completing Any Task

### 1. Code Quality (REQUIRED)
```bash
# Run on all changed files
uv run ruff check <changed_files> && uv run ruff format <changed_files>
```

### 2. Run Tests (if applicable)
```bash
# Run relevant tests
uv run pytest tests/unit  # For unit tests
uv run pytest tests/integration  # For integration tests
```

### 3. Documentation
- Check if related documentation needs updating
- Key docs to check:
  - `docs/reference/plausible.md` - for analytics events
  - `docs/workflows/` - for workflow changes
  - `docs/contributing.md` - for user-facing changes

## CRITICAL Rules

### Do NOT:
- Commit or push in interactive sessions (let user do it)
- Manually create `plots/{spec-id}/` directories
- Manually write `specification.md` files
- Manually merge implementation PRs
- Upload images to GCS manually

### Always:
- Use the GitHub Actions workflow for specs and implementations
- Add `approved` label to ISSUES (not PRs)
- Let `impl-merge.yml` handle PR merging
- Update documentation when changing features

## For Spec/Implementation Changes
All specifications and implementations MUST go through the GitHub Actions pipeline:

1. Create GitHub Issue with descriptive title (NO spec-id!)
2. Add `spec-request` label
3. Wait for `spec-create.yml` to create PR
4. Add `approved` label to the ISSUE
5. Wait for merge and `spec-ready` label
6. Trigger `bulk-generate.yml` for implementations
7. DO NOT manually merge - let workflows handle it
