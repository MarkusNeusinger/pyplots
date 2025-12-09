# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Rules

- **Do NOT commit or push in interactive sessions** - When working with a user interactively, never run `git commit` or `git push` automatically. Always let the user review changes and commit/push manually.
- **GitHub Actions workflows ARE allowed to commit/push** - When running as part of `plot-*.yml` workflows, creating branches, commits, and PRs is expected and required.
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

### Plot-Centric Design

Everything for one plot type lives in a single directory:

```
plots/{spec-id}/
├── spec.md              # Description, Applications, Data, Notes
├── metadata.yaml        # Tags, generation info, quality history
└── implementations/     # Library implementations
    ├── matplotlib.py
    ├── seaborn.py
    ├── plotly.py
    ├── bokeh.py
    ├── altair.py
    ├── plotnine.py
    ├── pygal.py
    ├── highcharts.py
    └── letsplot.py
```

Example: `plots/scatter-basic/` contains everything for the basic scatter plot.

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

- **`plots/{spec-id}/`**: Plot-centric directories (spec, metadata, implementations together)
  - `spec.md`: Library-agnostic specification (Description, Applications, Data, Notes)
  - `metadata.yaml`: Tags, generation info, quality scores (synced to PostgreSQL)
  - `implementations/{library}.py`: Library-specific implementations
- **`prompts/`**: AI agent prompts for code generation, quality evaluation, and tagging
  - `templates/`: Spec and metadata templates
  - `library/`: Library-specific generation rules (9 files)
- **`core/`**: Shared business logic (database, repositories, config)
- **`api/`**: FastAPI backend (routers, schemas, dependencies)
- **`app/`**: React frontend (Vite + TypeScript + MUI)
- **`tests/unit/`**: Unit tests mirroring source structure
- **`docs/`**: Architecture and workflow documentation

### Key Architecture Patterns

1. **Repository Pattern**: Data access layer in `core/repositories/`
2. **Async Everything**: FastAPI + SQLAlchemy async + asyncpg
3. **Clean Repo**: Only production code in git. Quality reports → GitHub Issues. Preview images → GCS.
4. **Issue-Based Workflow**: GitHub Issues as state machine for plot lifecycle

### Metadata System

Each plot directory contains a `metadata.yaml` file that is synced to PostgreSQL:

**File location:** `plots/{spec-id}/metadata.yaml`

```yaml
spec_id: scatter-basic
title: Basic Scatter Plot

# Spec-level tracking
created: 2025-01-10T08:00:00Z
issue: 42
suggested: CoolContributor123
updates:
  - date: 2025-01-15T10:30:00Z
    issue: 58
    changes: "Added Notes section"

# Spec-level tags (same for all library implementations)
tags:
  plot_type: [scatter, point]
  domain: [statistics, general]
  features: [basic, 2d, correlation]
  audience: [beginner]
  data_type: [numeric, continuous]

# Per-library implementation metadata (updated by plot-merge.yml)
implementations:
  matplotlib:
    preview_url: https://storage.googleapis.com/pyplots-images/plots/scatter-basic/matplotlib/plot.png
    current:
      generated_at: 2025-01-15T10:30:00Z
      generated_by: claude-opus-4-5-20251101
      workflow_run: 12345678
      issue: 42
      quality_score: 92
    history:
      - version: 1
        generated_at: 2025-01-10T08:00:00Z
        generated_by: claude-sonnet-4-20250514
        quality_score: 78
        feedback: |
          Missing grid lines.
          Font sizes too small.
        improvements_suggested:
          - "Add grid with alpha=0.3"
          - "Increase font sizes to 16+"
```

**Key points:**
- Spec-level tracking: `created`, `issue`, `suggested`, `updates`
- Contributors credited via `suggested` field
- Tags are at spec level (same for all libraries)
- Per-library metadata updated automatically by `plot-merge.yml` after each library PR merge
- Quality scores flow from `plot-review.yml` via PR labels (`quality:XX`)
- `sync-postgres.yml` workflow syncs to database on push to main
- Database stores full spec content (markdown) and implementation code (Python source)

### GCS Storage Structure

Preview images are stored in Google Cloud Storage (`pyplots-images` bucket):

```
gs://pyplots-images/
├── staging/{spec-id}/{library}/         # Temp images (during generation/review)
│   ├── plot.png                         # Generated by plot-generator.yml
│   └── plot.html                        # Optional (interactive libraries)
│
└── plots/{spec-id}/{library}/           # Production images (after merge to main)
    ├── plot.png                         # Promoted by plot-merge.yml
    └── plot.html                        # Optional (interactive libraries)
```

**Flow:**
1. `plot-generator.yml` uploads to `staging/{spec-id}/{library}/`
2. `plot-review.yml` reads from staging for AI evaluation
3. `plot-merge.yml` promotes staging → production when feature branch merges to main

**Interactive libraries** (generate `.html`): plotly, bokeh, altair, highcharts, pygal, letsplot
**PNG only**: matplotlib, seaborn, plotnine

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

**Implementation Files** (in `plots/{spec-id}/implementations/`):
- `{library}.py`: One file per library (e.g., `matplotlib.py`, `seaborn.py`)

## Database

**Connection**: PostgreSQL via SQLAlchemy async + asyncpg

**Connection Modes** (priority order):
1. `DATABASE_URL` - Direct connection (local development via public IP)
2. `INSTANCE_CONNECTION_NAME` - Cloud SQL Connector (Cloud Run, uses IAM auth)

**Local Development**:
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your DATABASE_URL
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/pyplots

# Test connection
uv run python -c "from core.database import is_db_configured; print(is_db_configured())"
```

**What's Stored** (synced from `plots/{spec-id}/`):
- Spec content (full markdown from spec.md)
- Spec metadata (title, description, tags, structured_tags)
- Implementation code (full Python source)
- Implementation metadata (library, variant, quality score, generation info)
- GCS URLs for preview images
- Social media promotion queue

**What's in Repository** (source of truth):
- Everything in `plots/{spec-id}/`:
  - `spec.md` - specification description
  - `metadata.yaml` - tags and generation history
  - `implementations/*.py` - library implementations

**What's NOT Stored in DB**:
- Preview images (in GCS)
- Detailed quality reports (in GitHub Issues, summary in metadata)

**Migrations**: Managed with Alembic
```bash
# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Check current revision
uv run alembic current
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
  $(cat plots/scatter-basic/spec.md)
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

### Core Plot Pipeline (`plot-*.yml`)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **plot-prepare.yml** | `plot-request` label | Validates request, assigns spec-id, creates `plot/{spec-id}` branch, generates spec |
| **plot-orchestrator.yml** | `approved` label | Creates status table, dispatches 9 parallel generators in 3 batches |
| **plot-generator.yml** | Called by orchestrator | Reusable: generates one library (code → test → preview → PR) |
| **plot-review.yml** | PR opened from `auto/*` | AI quality review, adds `quality:XX` and `ai-approved`/`ai-rejected` labels |
| **plot-merge.yml** | `ai-approved` label | Auto-merges PR, updates metadata.yaml, promotes GCS images to production |

### Workflow Data Flow

```
Issue + plot-request label
    │
    ▼
plot-prepare.yml
    ├── Creates: plot/{spec-id} branch
    ├── Creates: plots/{spec-id}/spec.md
    ├── Creates: plots/{spec-id}/metadata.yaml
    └── Posts: spec ready comment
    │
    ▼ (maintainer adds `approved` label)
    │
plot-orchestrator.yml
    ├── Posts: status table comment (updates live)
    └── Dispatches 3 batches (3+3+3 libraries)
        │
        ▼ (parallel)
        │
plot-generator.yml (×9)
    ├── Generates implementation
    ├── Tests (MPLBACKEND=Agg)
    ├── Uploads preview to GCS staging
    └── Creates PR: auto/{spec-id}/{library} → plot/{spec-id}
        │
        ▼ (triggers on PR)
        │
plot-review.yml
    ├── AI evaluates code + image
    ├── Posts review comment
    ├── Adds label: quality:XX
    └── Adds label: ai-approved OR ai-rejected
        │
        ▼ (triggers on ai-approved)
        │
plot-merge.yml
    ├── Squash-merges PR
    ├── Updates metadata.yaml (quality_score, generated_at, etc.)
    └── When all 9 done: merges plot/{spec-id} → main, promotes GCS images
```

### Supporting Workflows

| Workflow | Purpose |
|----------|---------|
| **ci-lint.yml** | Ruff linting on PR |
| **ci-unittest.yml** | Unit tests on PR |
| **sync-postgres.yml** | Syncs plots/ to database on push to main |

### Feature Branch Architecture

Each spec uses a **feature branch workflow** with a live status table (no sub-issues):

```
Main Issue #42: "Ridgeline plot"
    │
    ├── plot-prepare.yml creates:
    │   ├── Branch: plot/ridgeline-basic
    │   ├── plots/ridgeline-basic/spec.md
    │   └── plots/ridgeline-basic/metadata.yaml
    │
    ├── plot-orchestrator.yml posts status table:
    │   │
    │   │  | Library    | Status    | PR   | Quality |
    │   │  |------------|-----------|------|---------|
    │   │  | matplotlib | ✅ Done   | #101 | 92      |
    │   │  | seaborn    | ✅ Done   | #102 | 88      |
    │   │  | plotnine   | 🔄 Review | #103 | -       |
    │   │  | ...        | ...       | ...  | ...     |
    │   │
    │   └── Dispatches 9 generators in 3 batches (parallel within batch)
    │
    └── Each library creates PR: auto/ridgeline-basic/{library} → plot/ridgeline-basic

When all 9 libraries complete:
    PR: plot/ridgeline-basic → main (squash merge)
    Issue #42 closed with "completed" label
```

**Key design decisions:**
- **No sub-issues** - Status tracked via live-updating table in main issue comment
- **PRs as state** - Each library PR carries labels (`ai-approved`, `quality:XX`)
- **Metadata per-library** - `plot-merge.yml` updates metadata.yaml immediately after each merge
- **Parallel batches** - 3 batches of 3 libraries to avoid GitHub rate limits
- **Feature branch isolation** - All library PRs target feature branch, not main
- **Clean git history** - Single squash merge to main per plot spec

## GitHub Issue Labels

The project uses a structured labeling system. Setup labels with:
```bash
bash .github/scripts/setup-labels.sh
```

### Library Labels (per-library tracking)

- **`library:matplotlib`**, **`library:seaborn`**, **`library:plotly`**, **`library:bokeh`**, **`library:letsplot`**
- **`library:altair`**, **`library:plotnine`**, **`library:pygal`**, **`library:highcharts`**

### Workflow Status Labels

- **`plot-request`** - Main issue requesting a new plot type
- **`in-progress`** - Generation is running
- **`completed`** - All library implementations merged successfully
- **`partial`** - Some libraries completed, some failed
- **`not-feasible`** - 3x failed, library cannot implement this plot
- **`update`** - Update request for existing spec (use with plot-request)
- **`test`** - Test issue, not a real plot request

### PR Labels (set by workflows)

- **`ai-attempt-1`**, **`ai-attempt-2`**, **`ai-attempt-3`** - Retry counter
- **`ai-review-failed`** - AI review action failed or timed out

### Approval Labels (Human vs AI distinction)

| Label | Meaning | Set by |
|-------|---------|--------|
| `approved` | Human approved for implementation | Maintainer manually |
| `ai-approved` | AI quality check passed (score >= 85) | Workflow automatically |
| `rejected` | Human rejected | Maintainer manually |
| `ai-rejected` | AI quality check failed (score < 85) | Workflow automatically |

### Quality Score Labels

Quality scores are added as labels in format `quality:XX` (e.g., `quality:92`, `quality:85`).

These are set automatically by `plot-review.yml` after AI evaluation and used by `plot-merge.yml` to update metadata.yaml.

### Development Labels

- **`bug`** - Something isn't working
- **`infrastructure`** - Workflow, backend, or frontend issues
- **`documentation`** - Documentation improvements
- **`enhancement`** - New feature or improvement

### Plot Request Workflow (Feature Branch + Parallel Per-Library)

1. User creates issue with descriptive title (e.g., "3D scatter plot with rotation animation")
2. Add `plot-request` label
3. **`plot-prepare.yml` automatically runs:**
   - Analyzes the request, assigns spec ID (e.g., `scatter-3d-animated`)
   - Creates feature branch: `plot/{spec-id}`
   - Generates spec file: `plots/{spec-id}/spec.md`
   - Creates metadata file: `plots/{spec-id}/metadata.yaml`
   - Posts comment with spec analysis (waits for approval)
4. Maintainer reviews spec and adds `approved` label
5. **`plot-orchestrator.yml` triggers:**
   - Posts live status table comment (PR numbers, quality scores)
   - Dispatches 9 generators in 3 batches (parallel within batch)
6. **Each library (via `plot-generator.yml`):**
   - Generates implementation (separate Claude context)
   - Tests with `MPLBACKEND=Agg`
   - Uploads preview to GCS staging
   - Creates PR: `auto/{spec-id}/{library}` → `plot/{spec-id}`
7. **`plot-review.yml` triggers on each PR:**
   - AI evaluates code quality and visual output
   - Posts review comment with score
   - Adds labels: `quality:XX`, `ai-approved` or `ai-rejected`
   - If rejected: triggers retry (max 3 attempts)
8. **`plot-merge.yml` triggers on `ai-approved`:**
   - Squash-merges PR to feature branch
   - Updates `metadata.yaml` with quality score, timestamp, model
   - When all 9 done: creates PR `plot/{spec-id}` → `main`, enables auto-merge
   - Promotes GCS images from staging to production

**Benefits:**
- **~8x faster** (parallel execution within batches)
- **No sub-issues** (status tracked via live table in main issue)
- **Partial success** (6/9 can merge while 3/9 retry)
- **Clean git history** (single squash merge to main)
- **Traceable data** (quality scores flow via labels → metadata.yaml)

### Updating Existing Plots

To update an existing plot implementation:

1. Create issue with title: `[update] {spec-id}` (all libraries) or `[update:{library}] {spec-id}` (single library)
   - Example: `[update] scatter-basic` - regenerate all 9 libraries
   - Example: `[update:seaborn] scatter-basic` - regenerate only seaborn
2. Add label: `plot-request`
3. Issue body can contain spec changes (Claude will update `plots/{spec-id}/spec.md` first)
4. Maintainer adds `approved` label
5. Workflow regenerates specified implementations

**Issue Lifecycle:**
```
[open] plot-request → approved → in-progress → completed [closed]
                                             → partial [closed]
```

**Library PR Lifecycle:**
```
[open] → ai-approved → merged [closed]
      → ai-rejected → ai-attempt-1 → ai-attempt-2 → ai-attempt-3 → not-feasible [closed]
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
5. AI automatically generates `plots/{spec-id}/` directory with spec.md, metadata.yaml, and implementations
6. Multi-LLM quality check runs automatically on PR
7. Human reviews PR and merges

### Updating an Existing Implementation

1. Create GitHub Issue referencing original spec
2. Update implementation file in `plots/{spec-id}/implementations/{library}.py`
3. Run tests: `uv run pytest tests/unit/plots/test_{spec_id}.py`
4. Generate preview by running implementation standalone
5. Create PR with new preview
6. Quality check runs automatically

### Testing Plot Generation Locally

```bash
# Run implementation file directly
python plots/scatter-basic/implementations/matplotlib.py
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
