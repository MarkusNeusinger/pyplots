# Suggested Commands

## Development Setup
```bash
# Install all dependencies
uv sync --all-extras

# Start backend API
uv run uvicorn api.main:app --reload --port 8000

# Run database migrations
uv run alembic upgrade head
```

## Testing
```bash
# Run all tests
uv run pytest

# Run only unit tests
uv run pytest tests/unit

# Run only integration tests
uv run pytest tests/integration

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test
uv run pytest tests/unit/api/test_routers.py::test_get_specs
```

## Code Quality (REQUIRED before commits!)
```bash
# Lint check
uv run ruff check .

# Auto-fix lint issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Before committing (ALWAYS run this on changed files):
uv run ruff check <files> && uv run ruff format <files>
```

## Frontend Development
```bash
cd app
yarn install
yarn dev          # Development server
yarn build        # Production build
```

## Database
```bash
# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Check current revision
uv run alembic current
```

## GitHub Workflow Commands
```bash
# Trigger implementation generation
gh workflow run bulk-generate.yml -f specification_id=<spec-id> -f library=all

# Monitor workflow runs
gh run list --workflow=impl-generate.yml
gh run list --workflow=impl-review.yml

# Create spec request issue
gh issue create --title "Plot Type Name" --label "spec-request" --body "Description"
```

## System Utilities
- `git` - Version control
- `ls`, `cd`, `find`, `grep` - File navigation/search
- `cat`, `head`, `tail` - File viewing
- `uv` - Python package management (replaces pip)
