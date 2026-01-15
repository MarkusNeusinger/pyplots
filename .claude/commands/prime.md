# Prime

> Quickly understand the pyplots codebase - structure, rules, and current state.

## Project Vision

@docs/concepts/vision.md

## Project Config

@pyproject.toml

## Quick Stats

```bash
# Repository overview
echo "=== Repository Stats ==="
echo "Plot specifications: $(ls -d plots/*/ 2>/dev/null | wc -l)"
echo "Python files: $(find api core automation tests -name '*.py' 2>/dev/null | wc -l)"
echo "Frontend files: $(find app/src -name '*.tsx' -o -name '*.ts' 2>/dev/null | wc -l)"
echo "Workflows: $(ls .github/workflows/*.yml 2>/dev/null | wc -l)"
echo "Prompts: $(find prompts -name '*.md' 2>/dev/null | wc -l)"
```

## Structure

```bash
# Key directories
ls -la api/ core/ app/src/ prompts/ .github/workflows/ 2>/dev/null | head -50

# Documentation
find docs -name "*.md" 2>/dev/null | sort
```

## Current State

```bash
# Git status
git status --short

# Recent activity
git log --oneline -10
```

## Summarize

After reading, provide:
1. **Purpose**: What does this project do?
2. **Architecture**: Key components and how they connect
3. **Workflow**: How specs become implementations
4. **Tech Stack**: Languages, frameworks, infrastructure
5. **Key Rules**: Critical constraints from CLAUDE.md
