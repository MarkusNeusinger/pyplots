# Directory Structure

## Root Level
```
pyplots/
├── api/              # FastAPI backend
├── app/              # React frontend
├── core/             # Shared business logic
├── plots/            # Plot specifications and implementations (253 specs)
├── prompts/          # AI agent prompts (24 files)
├── tests/            # Test suite
├── docs/             # Documentation
├── automation/       # Automation scripts
├── alembic/          # Database migrations
├── .github/workflows/ # GitHub Actions (13 workflows)
└── scripts/          # Utility scripts
```

## Key Directories

### `api/` - FastAPI Backend
- `main.py` - Application entry point
- `routers/` - API route handlers
- `schemas.py` - Pydantic models
- `dependencies.py` - Dependency injection
- `exceptions.py` - Error handlers

### `core/` - Shared Logic
- `config.py` - Configuration management
- `constants.py` - Project constants
- `database/` - Database models and connection
- `generators/` - Code generation utilities
- `images.py` - Image processing

### `app/src/` - React Frontend
- `components/` - React components
- `pages/` - Page components
- `hooks/` - Custom React hooks
- `types/` - TypeScript types
- `utils/` - Utility functions

### `plots/{spec-id}/` - Plot-Centric Design
```
plots/{specification-id}/
├── specification.md      # Library-agnostic description
├── specification.yaml    # Spec metadata (tags, created, issue)
├── metadata/             # Per-library metadata
│   ├── matplotlib.yaml
│   ├── seaborn.yaml
│   └── ...
└── implementations/      # Library implementations
    ├── matplotlib.py
    ├── seaborn.py
    └── ...
```

### `prompts/` - AI Prompts
- `plot-generator.md` - Base rules for implementations
- `library/*.md` - Library-specific rules (9 files)
- `quality-criteria.md` - Quality definition
- `quality-evaluator.md` - AI quality evaluation
- `spec-validator.md` - Spec validation
- `templates/` - Spec and metadata templates

### `.github/workflows/` - Automation
- `spec-create.yml` - Create new specifications
- `impl-generate.yml` - Generate implementations
- `impl-review.yml` - AI quality review
- `impl-repair.yml` - Fix rejected implementations
- `impl-merge.yml` - Merge approved PRs
- `bulk-generate.yml` - Batch generation
- `sync-postgres.yml` - Database sync
