# Task Completion Checklist

## Before Completing Any Task

### 1. Code Quality (REQUIRED)
```bash
# Python changes
uv run ruff check <changed_files> && uv run ruff format <changed_files>

# Frontend changes
cd app && yarn lint
```

### 2. Run Tests (if applicable)
```bash
uv run pytest tests/unit       # For backend changes
uv run pytest tests/integration  # For DB/API changes
cd app && yarn build           # For frontend (catches TS errors)
cd app && yarn test            # Frontend unit tests (vitest)
```

### 3. Documentation
Check if related docs need updating:
- `docs/reference/plausible.md` - analytics events
- `docs/workflows/` - workflow changes
- `docs/contributing.md` - user-facing changes
- `agentic/docs/project-guide.md` - architecture/agentic changes

## Critical Rules

### NEVER do:
- Commit or push in interactive sessions (let user do it)
- Manually create `plots/{spec-id}/` directories or `specification.md` files
- Manually merge implementation PRs
- Upload images to GCS manually
- Add `approved` label to PRs (add to ISSUES instead)

### ALWAYS do:
- Use GitHub Actions pipeline for specs and implementations
- Write everything in English
- Let `impl-merge.yml` handle PR merging
- Update docs when changing features or workflows
