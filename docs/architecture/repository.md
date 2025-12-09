# 📁 Repository Structure

## Overview

pyplots follows a **plot-centric repository pattern** where everything for one plot type lives in a single directory:

```
plots/{spec-id}/
├── spec.md              # Description, data requirements, use cases
├── metadata.yaml        # Tags, generation info, quality history
└── implementations/     # Library implementations
    ├── matplotlib.py
    ├── seaborn.py
    └── ...
```

**Key Principle**: The repository contains **only production code and final specs**. Quality reports and workflow state are managed in GitHub Issues. Preview images are stored in GCS.

---

## Directory Layout

```
pyplots/
├── plots/                             # Plot-centric directories
│   ├── scatter-basic/                 # Everything for basic scatter plot
│   │   ├── spec.md                    # Library-agnostic specification
│   │   ├── metadata.yaml              # Tags, generation info, quality scores
│   │   └── implementations/           # Library-specific code
│   │       ├── matplotlib.py
│   │       ├── seaborn.py
│   │       ├── plotly.py
│   │       ├── bokeh.py
│   │       ├── altair.py
│   │       ├── plotnine.py
│   │       ├── pygal.py
│   │       ├── highcharts.py
│   │       └── letsplot.py
│   │
│   ├── bar-basic/
│   │   ├── spec.md
│   │   ├── metadata.yaml
│   │   └── implementations/
│   │       └── ...
│   │
│   └── heatmap-correlation/
│       ├── spec.md
│       ├── metadata.yaml
│       └── implementations/
│           └── ...
│
├── templates/                         # Templates for new specs
│   └── spec.md                        # Spec file template
│
├── prompts/                           # AI agent prompts
│   ├── plot-generator.md              # Base rules for code generation
│   ├── quality-criteria.md            # Quality evaluation criteria
│   ├── quality-evaluator.md           # Multi-LLM evaluation prompt
│   ├── auto-tagger.md                 # Automatic tagging
│   ├── spec-validator.md              # Validates plot requests
│   ├── spec-id-generator.md           # Assigns spec IDs
│   └── library/                       # Library-specific rules
│       ├── matplotlib.md
│       ├── seaborn.md
│       └── ...
│
├── core/                              # Shared business logic
│   ├── __init__.py
│   ├── config.py                      # Configuration (.env-based)
│   └── database/                      # Database layer
│       ├── __init__.py
│       ├── connection.py              # Async connection management
│       ├── models.py                  # SQLAlchemy ORM models
│       └── repositories.py            # Repository pattern
│
├── api/                               # FastAPI backend
│   ├── __init__.py
│   ├── main.py                        # Application entry point
│   └── Dockerfile                     # Cloud Run deployment
│
├── app/                               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── package.json
│   └── Dockerfile
│
├── scripts/                           # Utility scripts
│   └── sync_to_postgres.py            # Sync plots/ to database
│
├── tests/                             # Test suite
│   └── unit/
│       ├── api/
│       ├── core/
│       ├── prompts/
│       └── workflows/
│
├── .github/
│   └── workflows/                     # GitHub Actions CI/CD
│       ├── gen-create-spec.yml        # Creates feature branch + spec
│       ├── gen-new-plot.yml           # Orchestrator for parallel generation
│       ├── gen-library-impl.yml       # Per-library implementation
│       ├── ci-plottest.yml            # Multi-Python testing
│       ├── gen-preview.yml            # Preview image generation
│       ├── bot-ai-review.yml          # AI quality evaluation
│       ├── bot-auto-merge.yml         # Auto-merge approved PRs
│       ├── sync-postgres.yml          # Sync to database on push
│       └── ...
│
├── alembic/                           # Database migrations
│   └── versions/
│
├── docs/                              # Documentation
│   ├── architecture/
│   ├── workflow.md
│   ├── specs-guide.md
│   └── development.md
│
├── pyproject.toml                     # Python project config (uv)
├── uv.lock                            # Dependency lock file
├── .env.example                       # Environment variables template
├── CLAUDE.md                          # AI assistant instructions
└── README.md
```

---

## Key Directories Explained

### `plots/{spec-id}/`

**Purpose**: Plot-centric directories containing everything for one plot type

**Structure**:
```
plots/{spec-id}/
├── spec.md              # Library-agnostic specification
├── metadata.yaml        # Tags, generation info, quality history
└── implementations/     # Library-specific implementations
    ├── matplotlib.py
    ├── seaborn.py
    └── ...
```

**Characteristics**:
- ✅ Self-contained (spec + metadata + code together)
- ✅ Easy to navigate (one folder = one plot type)
- ✅ Synced to PostgreSQL via `sync-postgres.yml`
- ❌ NO preview images (stored in GCS)
- ❌ NO quality reports (stored in GitHub Issues)

**Example**: `plots/scatter-basic/` contains everything for the basic scatter plot.

---

### `plots/{spec-id}/spec.md`

**Purpose**: Library-agnostic plot specification

**Contents**:
- Title and description
- Data requirements (columns, types)
- Use cases with domain context
- Visual requirements

**Naming**: Always `spec.md` (consistent across all plots)

---

### `plots/{spec-id}/metadata.yaml`

**Purpose**: Structured metadata synced to PostgreSQL

**Contents**:
```yaml
spec_id: scatter-basic
title: Basic Scatter Plot

tags:
  plot_type: [scatter, point]
  domain: [statistics, general]
  features: [basic, 2d]
  audience: [beginner]
  data_type: [numeric]

implementations:
  matplotlib:
    preview_url: https://storage.googleapis.com/...
    current:
      generated_at: 2025-01-15T10:30:00Z
      generated_by: claude-opus-4-5-20251101
      quality_score: 92
    history: []
```

**Key Points**:
- Tags are at spec level (same for all libraries)
- Generation info tracks AI model used
- History preserves previous attempts with feedback

---

### `plots/{spec-id}/implementations/`

**Purpose**: Library-specific Python implementations

**File Naming**: `{library}.py`
- `matplotlib.py`
- `seaborn.py`
- `plotly.py`
- `bokeh.py`
- `altair.py`
- `plotnine.py`
- `pygal.py`
- `highcharts.py`
- `letsplot.py`

**Code Style** (KISS):
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
ax.scatter(x, y, alpha=0.7, s=50)
ax.set_title('Basic Scatter Plot')

plt.tight_layout()
plt.savefig('plot.png', dpi=300)
```

**Rules**:
- No functions, no classes
- No `if __name__ == '__main__':`
- Just: imports → data → plot → save

---

### `templates/`

**Purpose**: Templates for creating new specs

**Files**:
- `spec.md` - Template for new spec files

---

### `prompts/`

**Purpose**: AI agent prompts for code generation and quality evaluation

**Files**:
- `plot-generator.md` - Base rules for all implementations
- `quality-criteria.md` - Definition of quality
- `quality-evaluator.md` - Multi-LLM evaluation
- `auto-tagger.md` - Automatic tagging
- `library/*.md` - Library-specific rules (9 files)

---

### `core/`

**Purpose**: Shared business logic used by API

**Key Components**:
- `database/connection.py` - Async database connection
- `database/models.py` - SQLAlchemy ORM models
- `database/repositories.py` - Repository pattern for data access

---

### `api/`

**Purpose**: FastAPI REST API

**Key Files**:
- `main.py` - FastAPI app with all endpoints

---

### `app/`

**Purpose**: React frontend (Vite + TypeScript + MUI)

---

### `.github/workflows/`

**Purpose**: CI/CD automation via GitHub Actions

**Key Workflows**:
- `gen-create-spec.yml` - Creates feature branch and spec file
- `gen-new-plot.yml` - Orchestrates parallel library generation
- `gen-library-impl.yml` - Generates one library implementation
- `ci-plottest.yml` - Multi-Python version testing
- `gen-preview.yml` - Generates preview images
- `bot-ai-review.yml` - AI quality evaluation
- `sync-postgres.yml` - Syncs plots/ to database

---

## Naming Conventions

### Spec IDs

Format: `{type}-{variant}` or `{type}-{variant}-{modifier}`

**Examples**:
- `scatter-basic` - Basic scatter plot
- `scatter-color-groups` - Scatter with color-coded groups
- `bar-grouped-horizontal` - Horizontal grouped bars
- `heatmap-correlation` - Correlation matrix heatmap

**Rules**:
- All lowercase
- Hyphens as separators
- Descriptive names (no numbers needed)

### Implementation Files

Always named by library: `{library}.py`
- `matplotlib.py`, `seaborn.py`, `plotly.py`, etc.

---

## What's NOT in the Repository

### ❌ Preview Images
- **Where**: Google Cloud Storage (`gs://pyplots-images/plots/...`)
- **Why**: Binary files bloat git history

### ❌ Quality Reports
- **Where**: GitHub Issues (as bot comments)
- **Why**: Keeps repo clean, increases transparency

### ❌ Secrets
- **Where**: Environment variables, Cloud Secret Manager
- **Why**: Security
- **Note**: `.env.example` shows required variables without values

---

## Database Sync

The `sync-postgres.yml` workflow syncs `plots/` to PostgreSQL on push to main:

**What's Synced**:
- Spec content (full markdown from spec.md)
- Spec metadata (title, description, tags)
- Implementation code (full Python source)
- Implementation metadata (quality score, generation info)
- Preview URLs from metadata.yaml

**Source of Truth**: The `plots/` directory is authoritative. Database is derived.

---

*For implementation details, see [specs-guide.md](../specs-guide.md) and [development.md](../development.md)*
