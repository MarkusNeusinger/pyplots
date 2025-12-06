# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Rules

- **Do NOT commit or push in interactive sessions** - When working with a user interactively, never run `git commit` or `git push` automatically. Always let the user review changes and commit/push manually.
- **GitHub Actions workflows ARE allowed to commit/push** - When running as part of `spec-to-code.yml` or other automated workflows, creating branches, commits, and PRs is expected and required.
- **No Co-authored-by in commit messages** - Never add `Co-authored-by:` lines to commit messages. Keep commit messages clean without AI attribution footers.
- **Always write in English** - All output text (code comments, commit messages, PR descriptions, issue comments, documentation) must be in English, even if the user writes in another language.

## Project Overview

**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples. The platform is specification-driven: every plot starts as a library-agnostic Markdown spec, then AI generates implementations for all supported libraries.

**Supported Libraries** (9 total):
- **matplotlib** - The classic standard, maximum flexibility
- **seaborn** - Statistical visualizations, beautiful defaults
- **plotly** - Interactive web plots, dashboards, 3D
- **bokeh** - Interactive, streaming data, large datasets
- **altair** - Declarative/Vega-Lite, elegant exploration
- **plotnine** - ggplot2 syntax for R users
- **pygal** - Minimalistic SVG charts
- **highcharts** - Interactive web charts, stock charts (requires license for commercial use)
- **lets-plot** - ggplot2 grammar of graphics by JetBrains, interactive

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
specs/scatter-basic.md  → plots/matplotlib/scatter/scatter-basic/default.py
                        → plots/seaborn/scatterplot/scatter-basic/default.py
                        → plots/plotly/scatter/scatter-basic/default.py
                        → plots/bokeh/scatter/scatter-basic/default.py
                        → plots/altair/scatter/scatter-basic/default.py
                        → plots/plotnine/scatter/scatter-basic/default.py
                        → plots/pygal/scatter/scatter-basic/default.py
                        → plots/highcharts/scatter/scatter-basic/default.py
                        → plots/letsplot/point/scatter-basic/default.py
```

The same spec ID links implementations across all 9 supported libraries.

### Spec ID Naming Convention

**Format:** `{plot-type}-{variant}-{modifier}` (all lowercase, hyphens only)

- `plot-type`: Main visualization type (scatter, bar, line, heatmap, histogram, box, violin, pie, etc.)
- `variant`: Main characteristic (basic, grouped, stacked, horizontal, 3d, multi, etc.)
- `modifier`: Optional additional feature (regression, animated, interactive, annotated, etc.)

**Examples:**
- `scatter-basic` - Simple 2D scatter plot
- `scatter-color-mapped` - Scatter with color encoding
- `scatter-regression-linear` - Scatter with trend line
- `bar-grouped-horizontal` - Horizontal grouped bars
- `heatmap-correlation` - Correlation matrix heatmap
- `line-timeseries-multi` - Multiple time series

**Note:** Legacy specs may use numbered format (`scatter-basic-001`). Both formats are supported.

### Directory Structure

- **`specs/`**: Library-agnostic plot specifications (Markdown)
- **`plots/{library}/{plot_type}/{spec_id}/{variant}.py`**: Library-specific implementations
- **`core/`**: Shared business logic (database, repositories, config)
- **`api/`**: FastAPI backend (routers, schemas, dependencies)
- **`app/`**: React frontend (Vite + TypeScript + MUI)
- **`prompts/`**: AI agent prompts for code generation, quality evaluation, and tagging
- **`tests/unit/`**: Unit tests mirroring source structure
- **`docs/`**: Architecture and workflow documentation

### Key Architecture Patterns

1. **Repository Pattern**: Data access layer in `core/repositories/`
2. **Async Everything**: FastAPI + SQLAlchemy async + asyncpg
3. **Clean Repo**: Only production code in git. Quality reports → GitHub Issues. Preview images → GCS.
4. **Issue-Based Workflow**: GitHub Issues as state machine for plot lifecycle

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), PostgreSQL, Python 3.10+
- **Frontend**: React 19, Vite, TypeScript, MUI 7
- **Plotting**: matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, highcharts, lets-plot
- **Package Manager**: uv (fast Python installer)
- **Infrastructure**: Google Cloud Run, Cloud SQL, Cloud Storage
- **Automation**: GitHub Actions (code workflows) + n8n Cloud (external services)
- **AI**: Claude (code generation), Vertex AI (multi-LLM quality checks)

## Code Standards

### Python Style (API, Core, Tests)

- **Linter/Formatter**: Ruff (enforces PEP 8)
- **Line Length**: 120 characters
- **Type Hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Import Order**: Standard library → Third-party → Local

**Note:** Plot implementations in `plots/` follow a simpler KISS style - see "Implementation Guidelines" below.

Example (for API/core code):
```python
def get_spec_by_id(spec_id: str, db: Session) -> Spec:
    """
    Retrieve a spec by its ID.

    Args:
        spec_id: The unique spec identifier
        db: Database session

    Returns:
        Spec object if found

    Raises:
        NotFoundError: If spec doesn't exist
    """
    pass
```

### Testing Standards

- **Coverage Target**: 90%+
- **Test Structure**: Mirror source structure
- **Naming**: `test_{what_it_does}`
- **Fixtures**: Use pytest fixtures in `tests/conftest.py`

### File Naming Conventions

**Spec IDs**: `{type}-{variant}-{modifier}` (e.g., `scatter-basic`, `heatmap-correlation`)
- No numbers needed - descriptive names scale better
- See "Spec ID Naming Convention" section above for details

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

## Prompts System

The `prompts/` directory contains AI agent prompts for code generation, quality evaluation, and tagging.

### Prompt Files

| File | Purpose |
|------|---------|
| `plot-generator.md` | Base rules for all plot implementations |
| `library/*.md` | Library-specific rules (9 files) |
| `quality-criteria.md` | Definition of code/visual quality |
| `quality-evaluator.md` | Multi-LLM evaluation prompt |
| `auto-tagger.md` | Automatic tagging across 5 dimensions |
| `spec-validator.md` | Validates plot request issues |
| `spec-id-generator.md` | Assigns unique spec IDs |

### Using Prompts

```bash
# View a prompt
cat prompts/plot-generator.md
cat prompts/library/matplotlib.md

# Edit a prompt
vim prompts/quality-criteria.md
git commit -m "prompts: improve quality criteria"
```

**No folder versioning** - Git history tracks all changes. View old versions with `git log -p prompts/*.md`.

### Workflow Integration

Workflows reference prompts instead of embedding long instructions:

```yaml
# Example usage in workflow
prompt: |
  $(cat prompts/plot-generator.md)
  $(cat prompts/library/matplotlib.md)

  ## Spec
  $(cat specs/scatter-basic.md)
```

## Implementation Guidelines

### Plot Code Style (KISS)

Plot implementations should be **simple, readable scripts** - like matplotlib gallery examples:

```python
"""
scatter-basic: Basic Scatter Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(42)
x = np.random.randn(100)
y = x * 0.8 + np.random.randn(100) * 0.5

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(x, y, alpha=0.7, s=50, color='#306998')

ax.set_xlabel('X Value')
ax.set_ylabel('Y Value')
ax.set_title('Basic Scatter Plot')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

**Rules:**
- No functions, no classes
- No `if __name__ == '__main__':`
- No type hints or docstrings (in plot code)
- Just: imports → data → plot → save

### Anti-Patterns to Avoid

- No `preview.png` files in repository (use GCS)
- No `quality_report.json` files (use GitHub Issues)
- No hardcoded API keys (use environment variables)
- Avoid version-specific files unless necessary (prefer single `default.py` for Python 3.10-3.13)

## GitHub Actions Workflows

Located in `.github/workflows/`:

### Core Generation Pipeline (Feature Branch + Parallel Per-Library)

- **gen-create-spec.yml**: Creates feature branch `plot/{spec-id}` and generates spec file
- **gen-new-plot.yml**: Orchestrator - creates sub-issues and triggers parallel generation
- **gen-library-impl.yml**: Reusable workflow - generates one library implementation
- **ci-plottest.yml**: Multi-Python-version testing (3.11-3.13)
- **gen-preview.yml**: Generates preview images, uploads to GCS
- **bot-ai-review.yml**: Per-library AI quality evaluation
- **gen-update-plot.yml**: Per-library repair loop (max 3 attempts)
- **bot-auto-merge.yml**: Per-library auto-merge to feature branch, then feature branch to main
- **bot-sync-status.yml**: Syncs sub-issue status to main issue

### Supporting Workflows

- **bot-validate-request.yml**: Validates plot requests, assigns spec IDs
- **bot-auto-tag.yml**: AI-generated tagging after merge
- **ci-lint.yml**: Ruff linting
- **ci-unittest.yml**: Unit tests

### Feature Branch Architecture

Each spec uses a **feature branch workflow**:
```
Main Issue (plot-request + approved)
    │
    └── gen-create-spec.yml
        ├── Creates: plot/{spec-id} branch
        ├── Creates: specs/{spec-id}.md
        └── Dispatches: gen-new-plot.yml
            │
            ├── Sub-Issue: [spec-id] matplotlib implementation
            │   └── Branch: auto/{spec-id}/matplotlib → PR → plot/{spec-id}
            │
            ├── Sub-Issue: [spec-id] seaborn implementation
            │   └── Branch: auto/{spec-id}/seaborn → PR → plot/{spec-id}
            │
            └── ... (6 more libraries, all PRs target feature branch)

When all libraries complete:
    plot/{spec-id} → main (single merge with spec + all implementations)
```

Each library runs in **separate context** with **isolated dependencies**:
- All PRs target the feature branch, not main
- Feature branch contains spec file + all successful implementations
- Single merge to main when complete (cleaner git history)
- Partial success: failed libraries don't block successful ones

## GitHub Issue Labels

The project uses a structured labeling system. Setup labels with:
```bash
bash .github/scripts/setup-labels.sh
```

### Library Labels (per-library tracking)

- **`library:matplotlib`**, **`library:seaborn`**, **`library:plotly`**, **`library:bokeh`**, **`library:letsplot`**
- **`library:altair`**, **`library:plotnine`**, **`library:pygal`**, **`library:highcharts`**

### Workflow Status Labels

- **`plot-request:impl`** - Library implementation sub-issue (child of main plot-request)
- **`generating`** - Code is being generated
- **`testing`** - Tests are running
- **`reviewing`** - Quality review in progress
- **`merged`** - Successfully merged to main
- **`not-feasible`** - 3x failed, not implementable in this library
- **`completed`** - All library implementations complete
- **`update`** - Update request for existing spec (use with plot-request)
- **`test`** - Test issue, not a real plot request

### Approval Labels (Human vs AI distinction)

| Label | Meaning | Set by |
|-------|---------|--------|
| `approved` | Human approved for implementation | Maintainer manually |
| `ai-approved` | AI quality check passed (score >= 85) | Workflow automatically |
| `rejected` | Human rejected | Maintainer manually |
| `ai-rejected` | AI quality check failed (score < 85) | Workflow automatically |

### Quality Score Labels

- **`quality:excellent`** - Score >= 90
- **`quality:good`** - Score 85-89
- **`quality:needs-work`** - Score 75-84
- **`quality:poor`** - Score < 75

### Development Labels

- **`bug`** - Something isn't working
- **`infrastructure`** - Workflow, backend, or frontend issues
- **`documentation`** - Documentation improvements
- **`enhancement`** - New feature or improvement

### Plot Request Workflow (Feature Branch + Parallel Per-Library)

1. User creates issue with descriptive title (e.g., "3D scatter plot with rotation animation")
2. Add `plot-request` label
3. **`bot-validate-request.yml` automatically runs:**
   - Analyzes the request, assigns spec ID (e.g., `scatter-3d-animated`)
   - Or flags as duplicate
4. Maintainer reviews and adds `approved` label
5. **`gen-create-spec.yml` triggers:**
   - Creates feature branch: `plot/{spec-id}`
   - Claude generates spec file: `specs/{spec-id}.md`
   - Dispatches `gen-new-plot.yml`
6. **`gen-new-plot.yml` orchestrator triggers:**
   - Creates **9 sub-issues** (one per library)
   - Dispatches **9 parallel generation jobs** (all use feature branch as base)
7. **Each library independently:**
   - Generates implementation in separate Claude context
   - Creates own branch: `auto/{spec-id}/{library}` FROM `plot/{spec-id}`
   - Creates PR targeting **feature branch** (not main)
   - Runs tests (Python 3.11-3.13)
   - Generates preview image
   - AI quality review (score >= 85 required)
   - Auto-merge to feature branch if approved, or repair loop (max 3 attempts)
8. **When all libraries complete:**
   - Creates PR from `plot/{spec-id}` to `main`
   - Auto-merges with squash (single commit with spec + all implementations)
   - Closes main issue with completion summary

**Benefits:**
- ~8x faster (parallel execution)
- No context pollution (separate Claude sessions)
- Partial success (6/9 can merge while 3/9 retry)
- Per-library dependency isolation
- **Clean git history** (single merge to main per plot)
- **Atomic feature** (spec + all implementations together)

### Updating Existing Plots

To update an existing plot implementation:

1. Create issue with title: `[update] {spec-id}` (all libraries) or `[update:{library}] {spec-id}` (single library)
   - Example: `[update] scatter-basic` - regenerate all 9 libraries
   - Example: `[update:seaborn] scatter-basic` - regenerate only seaborn
2. Add label: `plot-request`
3. Issue body can contain spec changes (Claude will update `specs/{spec-id}.md` first)
4. Maintainer adds `approved` label
5. Workflow regenerates specified implementations

**Issue Lifecycle:**
```
[open] plot-request → approved → in-progress → completed [closed]
```

**Sub-Issue Lifecycle:**
```
[open] generating → testing → reviewing → merged [closed]
                                        → not-feasible [closed]
```

**Test Issues:** When creating issues for testing workflows, add the `test` label to exclude them from production searches.

## Environment Variables

Required in `.env` for local development:
```bash
# Database (Cloud SQL via public IP for local dev)
DATABASE_URL=postgresql+asyncpg://user:password@CLOUD_SQL_IP:5432/pyplots

# Google Cloud Storage
GCS_BUCKET=pyplots-images
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Environment
ENVIRONMENT=development
```

**Production** (Cloud Run): Secrets are injected via Secret Manager and environment variables set in `cloudbuild.yaml`.

See `.env.example` for full list with comments.

## Common Development Tasks

### Adding a New Plot Type

1. Create GitHub Issue with descriptive title (e.g., "Grouped bar chart with error bars")
2. Add label `plot-request`
3. `validate-plot-request.yml` automatically assigns a spec ID (e.g., `bar-grouped-errorbars`)
4. Maintainer reviews and adds `approved` label
5. AI automatically generates spec file in `specs/` and implementations
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

The project runs on **Google Cloud Platform**:

| Service | Component | Purpose |
|---------|-----------|---------|
| **Cloud Run** | `pyplots-backend` | FastAPI API (auto-scaling, serverless) |
| **Cloud Run** | `pyplots-frontend` | React SPA served via nginx |
| **Cloud SQL** | PostgreSQL | Database (connected via Unix socket) |
| **Cloud Storage** | `pyplots-images` | Preview images (GCS bucket) |
| **Secret Manager** | `DATABASE_URL` | Secure credential storage |
| **Cloud Build** | Triggers | Auto-deploy on push to main |

### Automatic Deployment

Push to `main` branch triggers Cloud Build:
- Changes in `api/`, `core/`, `pyproject.toml` → Backend redeploy
- Changes in `app/` → Frontend redeploy

### Manual Deployment

```bash
# Backend
gcloud builds submit --config=api/cloudbuild.yaml --project=YOUR_PROJECT_ID

# Frontend
gcloud builds submit --config=app/cloudbuild.yaml --project=YOUR_PROJECT_ID
```

### Configuration Files

- **`api/cloudbuild.yaml`**: Backend build + deploy (includes Cloud SQL connection)
- **`api/Dockerfile`**: Python 3.13 + uv + FastAPI
- **`app/cloudbuild.yaml`**: Frontend build + deploy
- **`app/Dockerfile`**: Multi-stage build (Node → nginx)

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

- **docs/development.md**: Development setup, testing, deployment
- **docs/workflow.md**: Automation flows (Discovery → Deployment → Social)
- **docs/specs-guide.md**: How to write plot specifications
- **docs/architecture/repository.md**: Directory structure
- **docs/architecture/api.md**: API endpoints reference
- **docs/architecture/database.md**: Database schema
- **prompts/README.md**: AI agent prompt system

## Project Philosophy

- **No manual coding**: AI generates and maintains all plot implementations
- **Spec improvements over code fixes**: If a plot has issues, improve the spec, not the code
- **Your data first**: Examples work with real user data, not fake data
- **Community-driven**: Anyone can propose plots via GitHub Issues
- **Multi-LLM quality**: Claude + Gemini + GPT ensure quality (score ≥85 required)
- **Full transparency**: All feedback documented in GitHub Issues, not hidden in repo files
