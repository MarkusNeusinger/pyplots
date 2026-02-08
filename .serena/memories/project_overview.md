# pyplots - Project Overview

## Purpose
**pyplots** is an AI-powered platform for Python data visualization that automatically discovers, generates, tests, and maintains plotting examples across 9 major libraries. Community proposes plot ideas via GitHub Issues → AI generates code → AI quality review → Deployed.

## Supported Libraries (9)
matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, highcharts, lets-plot

## Tech Stack
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy async, asyncpg, PostgreSQL
- **Frontend**: React 19, Vite 7, TypeScript 5, MUI 7, Emotion CSS-in-JS
- **Package Managers**: uv (Python), yarn (frontend)
- **Infrastructure**: Google Cloud Run, Cloud SQL, Cloud Storage (GCS)
- **AI**: Claude (code generation, quality review, spec creation)
- **CI/CD**: GitHub Actions (13 workflows, label-driven triggers)

## Directory Structure
```
pyplots/
├── api/                    # FastAPI backend
│   ├── main.py             # App factory, CORS, lifespan
│   ├── routers/            # health, specs, libraries, images, plots, stats,
│   │                       # download, proxy, seo, og_images, debug
│   ├── mcp/               # MCP server (server.py)
│   ├── schemas.py          # Pydantic response models
│   ├── dependencies.py     # DB session injection
│   ├── exceptions.py       # HTTP error handlers
│   ├── cache.py            # Caching layer
│   └── analytics.py        # Analytics tracking
├── core/                   # Shared business logic
│   ├── config.py           # Settings (pydantic-settings)
│   ├── constants.py        # SUPPORTED_LIBRARIES, quality thresholds
│   ├── images.py           # GCS image handling
│   ├── utils.py            # Shared utilities
│   ├── database/
│   │   ├── connection.py   # Async SQLAlchemy engine
│   │   ├── models.py       # ORM models (Spec, Implementation, Tag)
│   │   ├── repositories.py # Data access layer
│   │   └── types.py        # Custom types (PostgreSQL + SQLite compat)
│   └── generators/
│       └── plot_generator.py  # Plot code generation logic
├── app/                    # React frontend
│   └── src/
│       ├── components/     # 13 components (PlotCard, CodeBlock, FilterPanel, Header, Footer, etc.)
│       ├── pages/          # GalleryPage, SpecDetailPage, AboutPage
│       ├── hooks/          # useSpecs, useSpec, useLibraries, useDebounce, useMediaQuery, etc.
│       ├── types/          # TypeScript interfaces
│       ├── utils/          # api.ts (fetch-based API client)
│       └── theme.ts        # MUI theme config
├── agentic/                # AI workflow layer
│   ├── workflows/          # Composable phase scripts (Click CLI, uv inline headers)
│   │   ├── plan.py, build.py, test.py, review.py  # Individual phases
│   │   ├── plan_build.py, plan_build_test.py       # Orchestrators
│   │   ├── plan_build_test_review.py               # Full pipeline
│   │   └── modules/        # agent.py (execution, types), state.py (persistence)
│   ├── commands/           # 12 .md prompt templates ($1, $2, $ARGUMENTS vars)
│   ├── specs/              # quality-criteria.md, code-conventions.md
│   ├── docs/               # project-guide.md
│   └── runs/               # Runtime state (gitignored)
├── automation/             # CI/CD helper scripts
│   └── scripts/            # workflow_cli.py, label_manager.py, sync_to_postgres.py, workflow_utils.py
├── plots/                  # 267 specifications (plot-centric design)
│   └── {spec-id}/
│       ├── specification.md      # Library-agnostic description
│       ├── specification.yaml    # Tags, metadata
│       ├── implementations/      # {library}.py files
│       └── metadata/             # {library}.yaml files
├── prompts/                # AI prompt files
│   ├── plot-generator.md, quality-*.md, spec-*.md, impl-tags-generator.md
│   ├── default-style-guide.md    # Default visual style rules
│   ├── library/                  # 9 library-specific rule files
│   ├── templates/                # spec/metadata YAML/MD templates
│   └── workflow-prompts/         # ai-quality-review.md, impl-generate-claude.md,
│                                 # impl-repair-claude.md, report-analysis.md
├── tests/                  # pytest suite
│   ├── conftest.py         # Shared fixtures
│   ├── unit/
│   │   ├── api/            # test_routers, test_cache, test_analytics, test_proxy, mcp/
│   │   ├── core/           # test_config, test_constants, test_images, test_types, test_utils
│   │   ├── agentic/        # test_state, test_template, test_agent_*, test_orchestrator*
│   │   ├── automation/     # test_label_manager, test_sync_to_postgres, test_workflow_*
│   │   ├── workflows/      # test_workflows
│   │   └── prompts/        # test_prompts
│   ├── integration/        # test_repositories, api/test_api_endpoints
│   └── e2e/                # test_api_postgres (requires DATABASE_URL)
├── docs/                   # contributing, development, reference/, workflows/, concepts/
├── alembic/                # DB migrations (async engine)
├── .github/workflows/      # 13 GitHub Actions workflows
└── docker-compose.yml      # API + PostgreSQL + frontend
```

## GitHub Actions Workflows (13)
| Workflow | Purpose |
|----------|---------|
| `spec-create.yml` | Creates specs from issues labeled `spec-request` |
| `impl-generate.yml` | Generates implementation for one spec+library |
| `impl-review.yml` | AI quality review of implementations |
| `impl-repair.yml` | Fixes rejected implementations (max 3 attempts) |
| `impl-merge.yml` | Merges approved PRs, creates metadata, promotes GCS |
| `bulk-generate.yml` | Batch generation for multiple specs/libraries |
| `report-validate.yml` | Validates user-submitted issue reports |
| `sync-postgres.yml` | Syncs filesystem specs/impls to PostgreSQL |
| `sync-labels.yml` | Auto-syncs labels after manual PR merges |
| `ci-lint.yml` | Ruff linting on PRs |
| `ci-tests.yml` | Unit tests on PRs |
| `notify-deployment.yml` | Deployment notifications |
| `util-claude.yml` | Claude utility workflow |

## Data Flow
1. GitHub Issue + `spec-request` → `spec-create.yml` generates spec PR
2. `approved` label on Issue → spec merges, gets `spec-ready` label
3. `bulk-generate.yml` → `impl-generate.yml` → `impl-review.yml` → `impl-merge.yml`
4. `sync-postgres.yml` syncs filesystem to PostgreSQL on push to main
5. FastAPI serves data, React frontend displays gallery at pyplots.ai
