# 🛠️ Development Guide

## Getting Started

### Prerequisites

**Required**:
- Python 3.10+ (3.12 recommended)
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- PostgreSQL 15+ (for local development)

**Optional**:
- Docker (for containerized database)
- Node.js 20+ (for frontend development)

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/pyplots.git
cd pyplots
```

### 2. Install Dependencies

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --all-extras
```

This installs:
- Core dependencies
- Development tools (pytest, ruff, mypy)
- All plotting libraries (matplotlib, seaborn, plotly)

### 3. Database Setup

**Option A: Local PostgreSQL**

```bash
# Create database
createdb pyplots

# Set environment variables
cp .env.example .env
# Edit .env and set DATABASE_URL
```

**Option B: Docker**

```bash
docker run -d \
  --name pyplots-postgres \
  -e POSTGRES_DB=pyplots \
  -e POSTGRES_USER=pyplots \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  postgres:15
```

### 4. Run Migrations

```bash
uv run alembic upgrade head
```

### 5. Start Backend

```bash
uv run uvicorn api.main:app --reload --port 8000
```

API available at: `http://localhost:8000`
Docs available at: `http://localhost:8000/docs`

### 6. Start Frontend (Optional)

```bash
cd app
npm install
npm run dev
```

Frontend available at: `http://localhost:3000`

---

## Environment Variables

Create `.env` file in project root (see `.env.example`):

```bash
# Database (Cloud SQL via public IP for local development)
DATABASE_URL=postgresql+asyncpg://user:password@CLOUD_SQL_PUBLIC_IP:5432/pyplots

# Google Cloud Storage
GCS_BUCKET=pyplots-images
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Environment
ENVIRONMENT=development

# API Keys (optional, for AI generation workflows)
# ANTHROPIC_API_KEY=sk-ant-...
```

**Production**: In Cloud Run, `DATABASE_URL` is injected from Secret Manager and uses a Unix socket connection to Cloud SQL.

**Never commit `.env`!** (Already in `.gitignore`)

---

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/unit/api/test_routers.py

# Run specific test
uv run pytest tests/unit/api/test_routers.py::test_get_specs
```

### Code Formatting

```bash
# Check formatting
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

### Type Checking (Optional)

```bash
# Install mypy first
uv sync --extra typecheck

# Then run type checking
uv run mypy .
```

**Note**: Type checking is optional. Ruff already catches most issues.

### Pre-commit Hook (Recommended)

```bash
# Install pre-commit
uv pip install pre-commit

# Install git hooks
pre-commit install

# Now formatting runs automatically on git commit
```

---

## Code Standards

See [CLAUDE.md](../CLAUDE.md) for detailed code standards including:
- Python style guide (PEP 8, Ruff)
- Type hints requirements
- Docstring format (Google style)
- Import ordering

---

## Testing

**Coverage Target**: 90%+

**Test Structure**: Mirror source structure (`plots/.../default.py` → `tests/unit/plots/.../test_*.py`)

**Test Naming**: `test_{what_it_does}`

**Fixtures**: Use pytest fixtures in `tests/conftest.py` for reusable test data

See [CLAUDE.md](../CLAUDE.md) for testing standards.

---

## Writing Plot Implementations

See [CLAUDE.md](../CLAUDE.md) for:
- Implementation file template
- Best practices (validation, defaults, error handling)
- Anti-patterns to avoid

---

## Contributing

### Proposing New Plots

**Option 1: GitHub Issue (Recommended)**

1. Create issue using spec template
2. Fill in description, requirements, use cases
3. Add label `plot-idea`
4. Wait for review and approval
5. AI generates implementations automatically

**Option 2: Pull Request (Advanced)**

1. Create spec directory: `plots/{spec-id}/` with spec.md
2. Implement for at least one library
3. Add tests
4. Create PR with previews
5. Wait for quality check and review

### Contribution Guidelines

**Before Submitting**:
- [ ] Code passes all tests (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] Type hints are present (`mypy`)
- [ ] Coverage is >90% for new code
- [ ] Docstrings are complete
- [ ] Preview image looks good

**PR Description Template**:

```markdown
## Description

Implements scatter-basic-001 for matplotlib

## Checklist

- [x] Spec file created/updated
- [x] Implementation code written
- [x] Tests added (coverage: 95%)
- [x] Preview generated
- [ ] Quality check passed (waiting for CI)

## Preview

![Preview](link-to-preview.png)

## Related Issue

Closes #123
```

---

## Project Structure

See [CLAUDE.md](../CLAUDE.md) for:
- Directory structure
- Implementation file naming (`plots/{spec-id}/implementations/{library}.py`)
- Test file naming (`tests/unit/plots/test_{spec_id}.py`)

---

## Common Tasks

### Add a New Library
1. Update database (add to `libraries` table)
2. Create directory structure (`mkdir -p plots/{library}/scatter`)
3. Implement existing specs
4. Add tests

### Update an Existing Implementation
1. Create GitHub issue referencing original
2. Update implementation file in `plots/{spec-id}/implementations/{library}.py`
3. Run tests: `uv run pytest tests/unit/plots/test_{spec_id}.py`
4. Create PR → Quality check runs automatically

---

## Debugging Tips

### Database Connection Issues

```bash
# Test connection
psql -U pyplots -d pyplots -h localhost

# Check migrations
uv run alembic current
uv run alembic history
```

### Import Errors

```bash
# Verify package installation
uv pip list

# Reinstall
uv sync --reinstall
```

### Plot Generation Errors

```python
# Run implementation standalone
python plots/scatter-basic/implementations/matplotlib.py

# Add debug prints
print(f"Data shape: {data.shape}")
print(f"Columns: {data.columns.tolist()}")
```

### Test Failures

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb
```

---

## FAQ

### Q: How do I add a completely new plot type?

**A**: Create GitHub issue with spec → AI generates code → Review and merge

### Q: What if I want to use a different plotting style?

**A**: Create style variant (e.g., `ggplot_style.py`, `dark_style.py`)

### Q: How do I test plot generation locally?

**A**: Run implementation file directly: `python plots/scatter-basic/implementations/matplotlib.py`

### Q: Do I need to implement for all libraries?

**A**: No! Start with one library. Others can be added later.

### Q: How do I handle Python version differences?

**A**: Only create version-specific files if absolutely necessary (e.g., syntax changes). Prefer single `default.py` that works across 3.10-3.13.

---

## Working with Rules

The project includes versioned rules for AI code generation and quality evaluation.

**Location**: `rules/` directory

**Key Files**:
- `rules/versions.yaml` - Version configuration
- `rules/generation/v*/` - Code generation rules (Markdown)
- `rules/README.md` - Rule system documentation

**Rule States**: draft → active → deprecated → archived

**See Also**:
- [A/B Testing Strategies](./concepts/ab-testing-rules.md)
- [Rules README](../rules/README.md)

---

## Deployment

pyplots runs on **Google Cloud Platform** (europe-west4 region):

| Service | Component | Purpose |
|---------|-----------|---------|
| **Cloud Run** | `pyplots-backend` | FastAPI API (serverless, auto-scaling) |
| **Cloud Run** | `pyplots-frontend` | React SPA via nginx |
| **Cloud SQL** | PostgreSQL 18 | Database (Unix socket in production) |
| **Cloud Storage** | `pyplots-images` | Preview images (GCS bucket) |
| **Secret Manager** | `DATABASE_URL` | Secure credential storage |
| **Cloud Build** | Triggers | Auto-deploy on push to main |

### Automatic Deployment (Recommended)

Push to `main` triggers Cloud Build automatically:
- `api/**`, `core/**`, `pyproject.toml` changes → Backend redeploy
- `app/**` changes → Frontend redeploy

### Manual Deployment

```bash
# Backend
gcloud builds submit --config=api/cloudbuild.yaml --project=YOUR_PROJECT_ID

# Frontend
gcloud builds submit --config=app/cloudbuild.yaml --project=YOUR_PROJECT_ID
```

### Key Files

- `api/cloudbuild.yaml` - Backend build config (Cloud SQL + Secrets)
- `api/Dockerfile` - Python 3.13 + uv + uvicorn
- `app/cloudbuild.yaml` - Frontend build config
- `app/Dockerfile` - Multi-stage: Node build → nginx serve

---

## Resources

**Documentation**:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pytest Docs](https://docs.pytest.org/)
- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)

**Tools**:
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Ruff Linter/Formatter](https://github.com/astral-sh/ruff)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

---

*For architecture details, see [architecture/](./architecture/)*
