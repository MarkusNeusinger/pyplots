# Commands Reference

## Development Setup
```bash
uv sync --all-extras                    # Install Python dependencies
cd app && yarn install                  # Install frontend dependencies
uv run alembic upgrade head             # Run DB migrations
```

## Running Services
```bash
uv run uvicorn api.main:app --reload --port 8000   # Backend API
cd app && yarn dev                                   # Frontend dev server
docker-compose up                                    # All services
```

## Code Quality (REQUIRED before commits)
```bash
uv run ruff check <files>              # Lint check
uv run ruff check <files> --fix        # Auto-fix lint
uv run ruff format <files>             # Format code
cd app && yarn lint                    # Frontend lint
```

## Testing
```bash
uv run pytest                          # All tests
uv run pytest tests/unit               # Unit tests only
uv run pytest tests/integration        # Integration tests
uv run pytest --cov=. --cov-report=html  # With coverage
uv run pytest tests/unit/api/test_routers.py::test_name  # Specific test
```

## Database
```bash
uv run alembic upgrade head            # Apply migrations
uv run alembic revision --autogenerate -m "description"  # Create migration
uv run alembic current                 # Check current revision
```

## Frontend
```bash
cd app && yarn dev                     # Dev server
cd app && yarn build                   # Production build (tsc + vite)
cd app && yarn preview                 # Preview prod build
cd app && yarn lint                    # ESLint check
cd app && yarn type-check              # TypeScript type check only
cd app && yarn test                    # Run vitest
cd app && yarn test:watch              # Watch mode tests
```

## Agentic Workflows
```bash
# Individual phases (all use Click CLI)
uv run agentic/workflows/plan.py --spec-id <id> --library <lib>
uv run agentic/workflows/build.py --run-id <id>
uv run agentic/workflows/test.py --run-id <id>
uv run agentic/workflows/review.py --run-id <id>

# Orchestrators
uv run agentic/workflows/plan_build.py --spec-id <id> --library <lib>
uv run agentic/workflows/plan_build_test.py --spec-id <id> --library <lib>
uv run agentic/workflows/plan_build_test_review.py --spec-id <id> --library <lib>
```

## GitHub Actions (via gh CLI)
```bash
# Spec workflow
gh issue create --title "Plot Name" --label "spec-request" --body "Description"
# After review: add 'approved' label to ISSUE (not PR!)

# Implementation workflow
gh workflow run bulk-generate.yml -f specification_id=<spec-id> -f library=all

# Monitor
gh run list --workflow=impl-generate.yml
gh run list --workflow=impl-review.yml
gh run list --workflow=impl-merge.yml

# Sync to DB
gh workflow run sync-postgres.yml
```

## Important Notes
- Use `uv run` for all Python commands (no system python)
- Use `yarn` (not npm) for frontend
- Never manually merge impl PRs - let `impl-merge.yml` handle it
