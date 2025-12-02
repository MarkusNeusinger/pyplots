# Copilot Instructions

This file provides guidance to GitHub Copilot when working with code in this repository.

## Important Rules

- **No Co-authored-by in commit messages** - Never add `Co-authored-by:` lines to commit messages. Keep commit messages clean without AI attribution footers.

## Project Overview

**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples. The platform is specification-driven: every plot starts as a library-agnostic Markdown spec, then AI generates implementations for all supported libraries.

**Supported Libraries** (8 total):
- matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, highcharts

**Core Principle**: Community proposes plot ideas via GitHub Issues → AI generates code → Multi-LLM quality checks → Deployed.

## Development Setup

```bash
# Install dependencies (uses uv - fast Python package manager)
uv sync --all-extras

# Run all tests
uv run pytest

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
                        → (and 5 more libraries...)
```

### Spec ID Naming Convention

**Format:** `{plot-type}-{variant}-{modifier}` (all lowercase, hyphens only)

Examples: `scatter-basic`, `scatter-color-mapped`, `bar-grouped-horizontal`, `heatmap-correlation`

### Directory Structure

- **`specs/`**: Library-agnostic plot specifications (Markdown)
- **`plots/{library}/{plot_type}/{spec_id}/{variant}.py`**: Library-specific implementations
- **`core/`**: Shared business logic (database, repositories, config)
- **`api/`**: FastAPI backend (routers, schemas, dependencies)
- **`app/`**: React frontend (React 19 + TypeScript + Vite 7 + MUI 7)
- **`rules/`**: Versioned rules for AI code generation and quality evaluation
- **`tests/unit/`**: Unit tests mirroring source structure
- **`docs/`**: Architecture and workflow documentation

## GitHub Issue Labels

### Workflow Status Labels

- **`plot-request`** - Main plot request issue
- **`plot-request:impl`** - Library implementation sub-issue (child of main)
- **`generating`** - Code is being generated
- **`testing`** - Tests are running
- **`reviewing`** - Quality review in progress
- **`merged`** - Successfully merged to main
- **`not-feasible`** - 3x failed, not implementable in this library
- **`completed`** - All library implementations complete
- **`update`** - Update request for existing spec
- **`test`** - Test issue, not a real plot request

### Updating Existing Plots

To update an existing plot:
1. Create issue with title: `[update] {spec-id}` (all libraries) or `[update:library] {spec-id}` (single library)
2. Add label: `plot-request`
3. Issue body can contain spec changes (Claude updates spec first)
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

## Code Standards

### Python Style

- **Linter/Formatter**: Ruff (enforces PEP 8)
- **Line Length**: 120 characters
- **Type Hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Import Order**: Standard library → Third-party → Local

### Testing Standards

- **Coverage Target**: 90%+
- **Test Structure**: Mirror source structure in `tests/unit/`
- **Naming**: `test_{what_it_does}`
- **Fixtures**: Use pytest fixtures in `tests/conftest.py`

### Plot Implementation Template

Every implementation file should:
1. Start with docstring describing spec ID, library, variant
2. Define `create_plot()` function with type hints
3. Validate inputs first (empty data, missing columns)
4. Validate data types (numeric columns)
5. Use sensible defaults (`figsize=(16, 9)`, `alpha=0.6`)
6. Include grid for readability
7. Return the Figure object

### Anti-Patterns to Avoid

- No `preview.png` files in repository (use GCS)
- No `quality_report.json` files (use GitHub Issues)
- No hardcoded API keys (use environment variables)

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), PostgreSQL, Python 3.10+
- **Frontend**: React 19, TypeScript, Vite 7, MUI 7
- **Package Manager**: uv (Python), yarn (Node.js)
- **Linting**: Ruff (Python)

## Deployment

The project runs on **Google Cloud Platform** (europe-west4 region):

| Service | Component | Purpose |
|---------|-----------|---------|
| **Cloud Run** | `pyplots-backend` | FastAPI API (auto-scaling, serverless) |
| **Cloud Run** | `pyplots-frontend` | React SPA served via nginx |
| **Cloud SQL** | PostgreSQL 15 | Database (Unix socket in production) |
| **Cloud Storage** | `pyplots-images` | Preview images (GCS bucket) |
| **Secret Manager** | `DATABASE_URL` | Secure credential storage |
| **Cloud Build** | Triggers | Auto-deploy on push to main |

Automatic deployment on push to `main`:
- `api/**`, `core/**`, `pyproject.toml` changes → Backend redeploy
- `app/**` changes → Frontend redeploy

## Acceptance Criteria

Before completing any task:
1. All tests pass: `uv run pytest`
2. Code passes linting: `uv run ruff check .`
3. Code is properly formatted: `uv run ruff format --check .`
4. Type hints are included for all new functions
5. Docstrings follow Google style for public functions
