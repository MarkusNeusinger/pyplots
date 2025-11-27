# 📁 Repository Structure

## Overview

pyplots follows a **mono-repository pattern** with clear separation between:
- Generic, library-agnostic specifications (Markdown)
- Library-specific implementations (Python code)
- Shared business logic and API
- Frontend application

**Key Principle**: The repository contains **only production code and final specs**. Quality reports, feedback, and workflow state are managed in GitHub Issues.

---

## Directory Layout

```
pyplots/
├── specs/                             # Generic plot specifications (Markdown)
│   ├── scatter-basic-001.md           # From GitHub Issue → Markdown Spec
│   ├── heatmap-corr-002.md
│   ├── timeseries-line-003.md
│   └── bar-grouped-004.md
│
├── rules/                             # Versioned rules for code generation and quality evaluation
│   ├── README.md                      # Rule system documentation
│   ├── versions.yaml                  # Index of all rule versions
│   ├── templates/                     # Templates for creating new rules
│   │   ├── generation-rules-template.md
│   │   ├── quality-criteria-template.md
│   │   └── evaluation-prompt-template.md
│   └── generation/                    # Code generation rules
│       └── v1.0.0-draft/             # Initial draft version
│           ├── metadata.yaml
│           ├── code-generation-rules.md
│           ├── quality-criteria.md
│           └── self-review-checklist.md
│
├── plots/                             # Library-specific implementations
│   ├── matplotlib/
│   │   ├── scatter/
│   │   │   ├── scatter-basic-001/     # Implements specs/scatter-basic-001.md
│   │   │   │   ├── default.py         # Standard implementation
│   │   │   │   ├── ggplot_style.py    # Style variant
│   │   │   │   └── py310.py           # Python 3.10 specific (only if needed)
│   │   │   └── scatter-advanced-005/
│   │   │       └── default.py
│   │   ├── bar/
│   │   │   └── bar-grouped-004/
│   │   │       └── default.py
│   │   └── heatmap/
│   │       └── heatmap-corr-002/
│   │           └── default.py
│   │
│   ├── seaborn/
│   │   ├── scatterplot/
│   │   │   └── scatter-basic-001/      # Same spec-id!
│   │   │       ├── default.py
│   │   │       └── darkgrid_style.py
│   │   └── heatmap/
│   │       └── heatmap-corr-002/
│   │           └── default.py
│   │
│   └── plotly/
│       └── scatter/
│           └── scatter-basic-001/      # Same spec-id!
│               └── default.py
│
├── core/                              # Shared business logic
│   ├── __init__.py
│   ├── database.py                    # Database connection management
│   ├── config.py                      # Configuration (.env-based)
│   ├── cache.py                       # Caching utilities
│   ├── models/                        # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── spec.py
│   │   ├── implementation.py
│   │   └── library.py
│   └── repositories/                  # Repository pattern
│       ├── __init__.py
│       ├── base.py
│       ├── spec_repo.py
│       └── implementation_repo.py
│
├── api/                               # FastAPI backend
│   ├── __init__.py
│   ├── main.py                        # Application entry point
│   ├── dependencies.py                # Dependency injection
│   ├── schemas.py                     # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── plots.py                   # Plot endpoints
│       ├── specs.py                   # Spec endpoints
│       └── data.py                    # Data upload
│
├── app/                               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── public/
│   ├── package.json
│   └── next.config.js
│
├── automation/                        # AI tools for code generation
│   ├── __init__.py
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── claude_generator.py        # Code generation
│   │   └── quality_checker.py         # Multi-LLM quality check
│   └── scripts/
│       ├── create_spec_from_issue.py
│       └── update_plots.py
│
├── tests/                             # Test suite
│   ├── unit/
│   │   ├── core/
│   │   │   └── test_repositories.py
│   │   ├── api/
│   │   │   └── test_routers.py
│   │   └── plots/
│   │       ├── matplotlib/
│   │       │   └── test_scatter_basic_001.py
│   │       └── seaborn/
│   │           └── test_scatter_basic_001.py
│   └── integration/
│       └── test_plot_pipeline.py
│
├── .github/
│   └── workflows/                     # GitHub Actions CI/CD
│       ├── spec-to-code.yml
│       ├── test-and-preview.yml
│       ├── quality-check.yml
│       └── deploy.yml
│
├── docs/                              # Documentation
│   ├── vision.md
│   ├── workflow.md
│   ├── architecture/
│   ├── development.md
│   └── deployment.md
│
├── scripts/                           # Utility scripts
│   ├── init_database.py
│   └── migrate.py
│
├── pyproject.toml                     # Python project config (uv)
├── uv.lock                            # Dependency lock file
├── .env.example                       # Environment variables template
├── .gitignore
├── README.md
└── Dockerfile                         # For Cloud Run deployment
```

---

## Key Directories Explained

### `specs/`

**Purpose**: Library-agnostic plot specifications in Markdown format

**Characteristics**:
- ✅ Created from approved GitHub Issues
- ✅ Markdown format (human and AI readable)
- ✅ Generic descriptions (no library-specific code)
- ✅ Versioned in git
- ❌ NO code implementations
- ❌ NO quality reports (those are in Issues)

**Naming**: `{type}-{variant}-{number}.md`
- Examples: `scatter-basic-001.md`, `heatmap-corr-002.md`

---

### `rules/`

**Purpose**: Versioned rules for AI code generation and quality evaluation

**Characteristics**:
- ✅ Markdown format (human and LLM readable)
- ✅ Semantic versioning (v1.0.0, v2.0.0, etc.)
- ✅ Separate generation and evaluation rules
- ✅ Templates for creating new versions
- ✅ Git-versioned for full audit trail

**Structure**: `rules/{type}/{version}/{files}.md`
- `type`: generation or evaluation
- `version`: Semantic version (v1.0.0)
- `files`: Rule Markdown files + metadata.yaml

**Versions**:
- **draft**: Work in progress (e.g., v1.0.0-draft)
- **active**: Production version
- **deprecated**: Superseded by newer version
- **archived**: Historical record

**Why Versioned Rules?**
- **Test improvements**: A/B test rule versions before deploying
- **Rollback capability**: Return to previous version if issues arise
- **Audit trail**: Know which rules generated which plots
- **Scientific improvement**: Prove new rules are better

**See Also**: [Rule Versioning Architecture](./rule-versioning.md)

---

### `plots/`

**Purpose**: Library-specific implementations organized by library and plot type

**Structure**: `plots/{library}/{plot_type}/{spec_id}/{variant}.py`
- `library`: matplotlib, seaborn, plotly, etc.
- `plot_type`: scatter, bar, heatmap, etc.
- `spec_id`: References spec file (e.g., scatter-basic-001)
- `variant`: default, style name, or Python version

**File Types**:
- `default.py` - Standard implementation (required)
- `{style}_style.py` - Style variants (e.g., `ggplot_style.py`, `darkgrid_style.py`)
- `py{version}.py` - Version-specific (only when necessary, e.g., `py310.py`)

**Important**:
- ❌ NO `preview.png` files (stored in GCS)
- ❌ NO `quality_report.json` (stored in GitHub Issues)
- ✅ Only Python code

**Cross-Library Linking**: Same `spec_id` across different libraries
```
matplotlib/scatter/scatter-basic-001/default.py
seaborn/scatterplot/scatter-basic-001/default.py
plotly/scatter/scatter-basic-001/default.py
```
All implement the same spec: `specs/scatter-basic-001.md`

---

### `core/`

**Purpose**: Shared business logic used by API and automation

**Key Files**:
- `database.py` - Database connection, async session management
- `config.py` - Environment variables, settings
- `cache.py` - Caching layer (if needed)

**Subdirectories**:
- `models/` - SQLAlchemy ORM models (database tables)
- `repositories/` - Repository pattern for data access

**Design Pattern**: Repository pattern separates data access from business logic

---

### `api/`

**Purpose**: FastAPI REST API serving frontend and automation

**Key Files**:
- `main.py` - FastAPI app initialization, CORS, middleware
- `dependencies.py` - Dependency injection (DB sessions, auth)
- `schemas.py` - Pydantic models for request/response validation

**Routers**:
- `plots.py` - Plot-related endpoints
- `specs.py` - Spec-related endpoints
- `data.py` - User data upload and plot generation

---

### `app/`

**Purpose**: Next.js frontend application

**Structure**: Standard Next.js 14 App Router structure
- `src/components/` - Reusable React components
- `src/pages/` - Page components
- `src/lib/` - Utilities and API client

---

### `automation/`

**Purpose**: AI-powered code generation and quality checking

**Key Files**:
- `generators/claude_generator.py` - Generates plot code from specs
- `generators/quality_checker.py` - Multi-LLM quality evaluation

**Usage**: Called by GitHub Actions, not part of production API

---

### `tests/`

**Purpose**: Comprehensive test suite (target: 90%+ coverage)

**Structure**:
- `unit/` - Unit tests for individual components
- `integration/` - End-to-end workflow tests

**Naming**: `test_{module_name}.py`

---

### `.github/workflows/`

**Purpose**: CI/CD automation via GitHub Actions

**Key Workflows**:
- `spec-to-code.yml` - Generate code from approved issues
- `test-and-preview.yml` - Run tests and create previews
- `quality-check.yml` - Multi-LLM quality evaluation
- `deploy.yml` - Deploy to Cloud Run

See [automation-workflows.md](./automation-workflows.md) for details.

---

## Naming Conventions

### Spec IDs

Format: `{type}-{variant}-{number}`

**Examples**:
- `scatter-basic-001` - Basic scatter plot
- `scatter-advanced-005` - Advanced scatter with multiple features
- `heatmap-corr-002` - Correlation heatmap
- `bar-grouped-004` - Grouped bar chart
- `timeseries-line-003` - Time series line plot

**Rules**:
- All lowercase
- Words separated by hyphens
- Three-digit number suffix (001, 002, etc.)
- Unique across all specs

### File Names

**Specs**: `{spec-id}.md`
- Example: `scatter-basic-001.md`

**Implementations**:
- Default: `default.py`
- Styles: `{style}_style.py` (e.g., `ggplot_style.py`)
- Version-specific: `py{version}.py` (e.g., `py310.py`, `py311.py`)

**Why version-specific files?**
Only create when necessary:
- Breaking changes between Python versions
- Library compatibility issues
- Syntax differences

Prefer: Single `default.py` that works across all versions (3.10-3.13)

---

## Code Organization Principles

### 1. Separation of Concerns

```
Specs (What)          →  plots/ (How)         →  tests/ (Verification)
Generic description      Library-specific code   Ensure correctness
```

### 2. DRY (Don't Repeat Yourself)

Shared logic goes in `core/`:
```python
# ✅ Good
from core.repositories import SpecRepository

# ❌ Bad
# Duplicate database queries in multiple routers
```

### 3. Dependency Flow

```
Frontend (app/) → API (api/) → Core (core/) → Database
                                       ↓
                              Plots (plots/)
```

### 4. Testing Parallel to Code

```
plots/matplotlib/scatter/scatter-basic-001/default.py
tests/unit/plots/matplotlib/test_scatter_basic_001.py
```

---

## What's NOT in the Repository

### ❌ Preview Images
- **Where**: Google Cloud Storage (`gs://pyplots-images/previews/...`)
- **Why**: Binary files bloat git history

### ❌ Quality Reports
- **Where**: GitHub Issues (as bot comments)
- **Why**: Keeps repo clean, increases transparency

### ❌ User Data
- **Where**: Processed in-memory, temporary files auto-deleted
- **Why**: Privacy and security

### ❌ Secrets
- **Where**: Environment variables, Cloud Secret Manager
- **Why**: Security
- **Note**: `.env.example` shows required variables without values

### ❌ n8n Workflows
- **Where**: n8n cloud/self-hosted instance
- **Why**: Visual workflows, not code-based
- **Note**: Can export JSON if needed for backup

---

## File Size Guidelines

### Specs
- Target: < 5 KB (readable Markdown)
- If larger: Consider splitting into multiple specs

### Implementation Files
- Target: < 500 lines per file
- If larger: Refactor into helper functions in `core/`

### Tests
- One test file per implementation
- Target: 100% coverage of plot generation logic

---

## Migration from Old Structure

If you have existing plots in a different structure:

**Old**: `plots/scatter_basic.py`
**New**: `plots/matplotlib/scatter/scatter-basic-001/default.py`

Run migration script:
```bash
python scripts/migrate_old_structure.py
```

---

*For implementation details and code examples, see [specs-guide.md](./specs-guide.md) and [development.md](../development.md)*
