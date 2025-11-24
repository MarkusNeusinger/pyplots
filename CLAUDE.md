# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples. The platform is specification-driven: every plot starts as a library-agnostic Markdown spec, then AI generates implementations for matplotlib, seaborn, plotly, and other libraries.

**Core Principle**: Community proposes plot ideas via GitHub Issues → AI generates code → Multi-LLM quality checks → Deployed.

## Essential Commands

### Development Setup

```bash
# Install dependencies (uses uv - fast Python package manager)
uv sync --all-extras

# Start backend API
uv run uvicorn api.main:app --reload --port 8000

# Run database migrations
uv run alembic upgrade head
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/unit/api/test_routers.py

# Run a single test
uv run pytest tests/unit/api/test_routers.py::test_get_specs
```

### Code Quality

```bash
# Check code formatting and linting
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

### Frontend Development

```bash
cd app
yarn install
yarn dev          # Development server
yarn build        # Production build
```

## Architecture

### Specification-First Design

Every plot follows this flow:
```
specs/{spec-id}.md → plots/{library}/{plot-type}/{spec-id}/default.py
```

Example:
```
specs/scatter-basic-001.md  → plots/matplotlib/scatter/scatter-basic-001/default.py
                            → plots/seaborn/scatterplot/scatter-basic-001/default.py
                            → plots/plotly/scatter/scatter-basic-001/default.py
```

The same spec ID links implementations across all libraries.

### Directory Structure

- **`specs/`**: Library-agnostic plot specifications (Markdown)
- **`plots/{library}/{plot_type}/{spec_id}/{variant}.py`**: Library-specific implementations
- **`core/`**: Shared business logic (database, repositories, config)
- **`api/`**: FastAPI backend (routers, schemas, dependencies)
- **`app/`**: Next.js frontend (React + TypeScript + Vite + MUI)
- **`rules/`**: Versioned rules for AI code generation and quality evaluation
- **`tests/unit/`**: Unit tests mirroring source structure
- **`docs/`**: Architecture and workflow documentation

### Key Architecture Patterns

1. **Repository Pattern**: Data access layer in `core/repositories/`
2. **Async Everything**: FastAPI + SQLAlchemy async + asyncpg
3. **Clean Repo**: Only production code in git. Quality reports → GitHub Issues. Preview images → GCS.
4. **Issue-Based Workflow**: GitHub Issues as state machine for plot lifecycle

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), PostgreSQL, Python 3.10+
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, MUI 7
- **Plotting**: matplotlib, seaborn, plotly
- **Package Manager**: uv (fast Python installer)
- **Infrastructure**: Google Cloud Run, Cloud SQL, Cloud Storage
- **Automation**: GitHub Actions (code workflows) + n8n Cloud (external services)
- **AI**: Claude (code generation), Vertex AI (multi-LLM quality checks)

## Code Standards

### Python Style

- **Linter/Formatter**: Ruff (enforces PEP 8)
- **Line Length**: 120 characters
- **Type Hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Import Order**: Standard library → Third-party → Local

Example:
```python
def create_plot(data: pd.DataFrame, x: str, y: str, **kwargs) -> Figure:
    """
    Create a scatter plot from DataFrame

    Args:
        data: Input DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        **kwargs: Additional plotting parameters

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If x or y column not found in data
    """
    pass
```

### Testing Standards

- **Coverage Target**: 90%+
- **Test Structure**: Mirror source structure
- **Naming**: `test_{what_it_does}`
- **Fixtures**: Use pytest fixtures in `tests/conftest.py`

### File Naming Conventions

**Spec IDs**: `{type}-{variant}-{number}` (e.g., `scatter-basic-001`)

**Implementation Variants**:
- `default.py`: Standard implementation (required)
- `{style}_style.py`: Style variants (e.g., `ggplot_style.py`)
- `py{version}.py`: Version-specific (only when necessary)

## Database

**Connection**: PostgreSQL via SQLAlchemy async + asyncpg

**What's Stored**:
- Spec metadata (title, description, tags)
- Implementation metadata (library, variant, quality score)
- GCS URLs for preview images
- Social media promotion queue

**What's NOT Stored**:
- Plot code (in repository)
- Preview images (in GCS)
- Quality reports (in GitHub Issues)

**Migrations**: Managed with Alembic
```bash
# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

## Versioned Rules System

The `rules/` directory contains versioned rules for AI code generation and quality evaluation.

### Working with Rules

```bash
# View current rules
cat rules/versions.yaml
cat rules/generation/v1.0.0-draft/code-generation-rules.md

# Create new version
cp -r rules/generation/v1.0.0-draft rules/generation/v1.1.0-draft
# Edit files, then update rules/versions.yaml
```

**Rule States**: draft → active → deprecated → archived

**Why Versioned?** Enables A/B testing of rule improvements, provides audit trail, allows rollback.

## Implementation Guidelines

### Plot Implementation Template

Every implementation file should:
1. Start with docstring describing spec ID, library, variant
2. Define `create_plot()` function with type hints
3. Validate inputs first (empty data, missing columns)
4. Use sensible defaults (`figsize=(10, 6)`, `alpha=0.8`)
5. Include grid for readability
6. Return the Figure object
7. Optionally include `if __name__ == '__main__':` for standalone testing

### Anti-Patterns to Avoid

- No `preview.png` files in repository (use GCS)
- No `quality_report.json` files (use GitHub Issues)
- No hardcoded API keys (use environment variables)
- Avoid version-specific files unless necessary (prefer single `default.py` for Python 3.10-3.13)

## GitHub Actions Workflows

Located in `.github/workflows/`:

- **spec-to-code.yml**: Generates code from approved specs
- **test-and-preview.yml**: Runs tests + creates preview images
- **quality-check.yml**: Multi-LLM quality evaluation
- **deploy.yml**: Deploys to Cloud Run

## GitHub Issue Labels

The project uses a structured labeling system to organize different types of issues:

### Plot-Related Labels

- **`plot-request`** (blue, `#0366d6`) - Community plot proposals
  - Use when: Someone proposes a new plot type or variant
  - Workflow: Add this label when creating an issue for a new plot
  - When combined with `approved`, triggers automatic code generation

- **`approved`** (green, `#0e8a16`) - Approved for implementation
  - Use when: A plot-request has been reviewed and accepted
  - Workflow: Triggers `spec-to-code.yml` workflow (if issue also has `plot-request` label)
  - Effect: Claude Code automatically generates implementations and creates PR

- **`quality-issue`** (orange, `#fb8500`) - Quality check found issues
  - Use when: Multi-LLM quality check identifies problems
  - Workflow: Automatically created by `quality-check.yml` workflow
  - Contains: Detailed quality report from Claude, Gemini, GPT evaluation

### Development Labels

- **`bug`** (red, `#d73a4a`) - Something isn't working
  - Use when: Existing plots have errors or incorrect behavior

- **`infrastructure`** (gray, `#6c757d`) - Workflow, backend, or frontend issues
  - Use when: Problems with GitHub Actions, API, database, or frontend

- **`documentation`** (blue, `#0075ca`) - Improvements or additions to documentation
  - Use when: Docs need updates or clarification

- **`enhancement`** (cyan, `#a2eeef`) - New feature or improvement to existing feature
  - Use when: Non-plot features (e.g., API endpoints, UI components)

### Plot Request Workflow Example

1. User creates issue titled `scatter-advanced-002: 3D scatter with rotation`
2. Add `plot-request` label
3. Maintainer reviews and adds `approved` label
4. `spec-to-code.yml` workflow automatically triggers
5. Claude Code generates implementations and creates PR
6. Tests run automatically on PR
7. Multi-LLM quality check evaluates code
8. Maintainer reviews and merges

## Environment Variables

Required in `.env`:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/pyplots
ANTHROPIC_API_KEY=sk-ant-...
GCS_BUCKET=pyplots-images-dev
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000
```

See `.env.example` for full list.

## Common Development Tasks

### Adding a New Plot Type

1. Create GitHub Issue with spec description (title format: `{spec-id}: Description`)
2. Add label `plot-request`
3. Maintainer reviews and adds `approved` label
4. AI automatically generates spec file in `specs/` (if needed)
5. AI generates implementations for matplotlib and seaborn
6. Multi-LLM quality check runs automatically on PR
7. Human reviews PR and merges

### Updating an Existing Implementation

1. Create GitHub Issue referencing original spec
2. Update implementation file
3. Run tests: `pytest tests/unit/plots/{library}/test_{spec_id}.py`
4. Generate preview by running implementation standalone
5. Create PR with new preview
6. Quality check runs automatically

### Adding a Style Variant

1. Create new file: `plots/{library}/{plot_type}/{spec_id}/{style}_style.py`
2. Add tests
3. Update database metadata
4. Generate preview

### Testing Plot Generation Locally

```bash
# Run implementation file directly
python plots/matplotlib/scatter/scatter_basic_001/default.py
```

## Cloud Deployment

### Backend (FastAPI)

```bash
# Deploy to Cloud Run
gcloud builds submit --config=api/cloudbuild.yaml --project=YOUR_PROJECT_ID
```

### Frontend (Next.js)

```bash
# Deploy to Cloud Run
gcloud builds submit --config=app/cloudbuild.yaml \
  --substitutions=_VITE_API_URL=https://api.pyplots.ai
```

## Debugging Tips

### Database Connection Issues
```bash
psql -U pyplots -d pyplots -h localhost
uv run alembic current
```

### Import Errors
```bash
uv pip list
uv sync --reinstall
```

### Test Failures
```bash
pytest -v          # Verbose
pytest -s          # Show prints
pytest --pdb       # Debug on failure
```

## Key Documentation Files

- **docs/development.md**: Comprehensive development guide
- **docs/architecture/repository-structure.md**: Detailed directory structure
- **docs/architecture/system-overview.md**: Architecture diagrams and data flows
- **docs/workflow.md**: 7 automation workflows (Discovery → Deployment → Social)
- **rules/README.md**: Rule versioning system documentation

## Project Philosophy

- **No manual coding**: AI generates and maintains all plot implementations
- **Spec improvements over code fixes**: If a plot has issues, improve the spec, not the code
- **Your data first**: Examples work with real user data, not fake data
- **Community-driven**: Anyone can propose plots via GitHub Issues
- **Multi-LLM quality**: Claude + Gemini + GPT ensure quality (score ≥85 required)
- **Full transparency**: All feedback documented in GitHub Issues, not hidden in repo files
