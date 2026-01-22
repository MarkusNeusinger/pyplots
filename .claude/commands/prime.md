# Prime

> Quickly understand the pyplots codebase - structure, rules, and current state.

## Project Vision

@docs/concepts/vision.md

## Project Config

@pyproject.toml

## Git Status

```bash
git status --short
git log --oneline -5
```

## Codebase Exploration

Use Serena MCP tools to explore:
- `list_dir(".", recursive=false)` - Top-level structure
- `list_dir("api/", recursive=true)` - Backend API structure
- `list_dir("core/", recursive=true)` - Core business logic
- `list_dir("app/src/", recursive=true)` - Frontend structure
- `jet_brains_get_symbols_overview` on `api/main.py`, `core/database/models.py` for key symbols

## Summarize

After exploring, provide:
1. **Purpose**: What does this project do?
2. **Architecture**: Key components and how they connect
3. **Workflow**: How specs become implementations
4. **Tech Stack**: Languages, frameworks, infrastructure
5. **Key Rules**: Critical constraints from CLAUDE.md
