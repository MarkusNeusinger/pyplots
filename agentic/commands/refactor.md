# Code Quality Refactor

> Comprehensive code quality analysis for the pyplots repository. Checks readability, performance, code smells, consistency, and modernization opportunities across all components.

## Context

@CLAUDE.md
@pyproject.toml

## Analysis Scope

Analyze the following areas systematically. For each area, identify:
- **Code Smells**: Dead code, duplication, overly complex functions, god classes
- **Readability**: Unclear naming, missing/outdated comments, inconsistent formatting
- **Performance**: Inefficient patterns, N+1 queries, unnecessary computations
- **Modernization**: Deprecated APIs, old Python patterns, outdated dependencies
- **Consistency**: Naming conventions, import styles, error handling patterns
- **Type Safety**: Missing type hints, incorrect types, Any overuse
- **Test Quality**: Missing tests, flaky tests, poor assertions

## Discover Structure

```bash
# Overview of repository structure
find . -type f -name "*.py" | grep -E "^\./(api|core|automation|tests)/" | head -80

# Frontend structure
find ./app/src -type f -name "*.ts" -o -name "*.tsx" 2>/dev/null | head -40

# Workflow files
ls -la .github/workflows/*.yml 2>/dev/null

# Prompt files
find ./prompts -type f -name "*.md" 2>/dev/null

# Documentation
find ./docs -type f -name "*.md" 2>/dev/null
```

## Run Quality Checks

```bash
# Linting issues
uv run ruff check .

# Format check (dry-run)
uv run ruff format . --check --diff
```

## Analyze Backend (api/)

Check for:
- Router organization and REST conventions
- Dependency injection patterns
- Error handling consistency
- Response schema completeness
- Async/await correctness
- Caching strategies

```bash
ls -la api/*.py api/**/*.py 2>/dev/null
```

## Analyze Core Logic (core/)

Check for:
- Repository pattern implementation
- Database model design
- Configuration management
- Utility function organization
- Type definitions

```bash
ls -la core/*.py core/**/*.py 2>/dev/null
```

## Analyze Automation (automation/)

Check for:
- Script modularity
- Error handling in workflows
- CLI argument parsing
- Logging consistency

```bash
ls -la automation/**/*.py 2>/dev/null
```

## Analyze Frontend (app/src/)

Check for:
- Component structure and reusability
- Hook patterns and custom hooks
- TypeScript strictness (no `any`, proper interfaces)
- Performance (memo, useCallback only where truly needed)
- Accessibility (aria-labels, keyboard navigation, focus management)
- Consistent error handling and error boundaries
- Loading states and skeletons
- Unused imports and dead code

```bash
ls -la app/src/**/*.tsx app/src/**/*.ts 2>/dev/null | head -30
```

## Analyze Tests (tests/)

Check for:
- Test coverage gaps
- Fixture organization
- Mock patterns
- Assertion quality
- Test naming conventions

```bash
find tests -name "*.py" -type f | head -30
```

## Analyze GitHub Workflows (.github/workflows/)

Check for:
- Workflow consistency and naming
- Job dependencies and parallelization
- Secret handling and security
- Error handling and failure modes
- Concurrency settings
- Reusable workflows vs duplication
- Environment variable consistency
- Trigger conditions (labels, paths, branches)

```bash
ls -la .github/workflows/*.yml
```

## Analyze AI Prompts (prompts/)

Check for:
- Prompt clarity and structure
- Consistency across prompt files
- Outdated instructions or references
- Missing edge cases
- Template completeness
- Library-specific rules alignment

```bash
find prompts -name "*.md" -o -name "*.yaml" | sort
```

## Analyze Documentation (docs/)

Check for:
- Outdated information vs actual code
- Missing documentation for new features
- Broken internal links
- Inconsistent formatting
- Sync with CLAUDE.md

```bash
find docs -name "*.md" | sort
```

## Cross-Check: Consistency

Verify alignment across components:
- Do workflows reference existing prompt files?
- Are library names consistent across `prompts/library/`, `core/constants.py`, workflows?
- Do workflow labels match documentation?
- Are schema definitions in sync between API and frontend types?

```bash
# Check prompt references in workflows
grep -r "prompts/" .github/workflows/ 2>/dev/null | head -20

# Library definitions
ls prompts/library/ 2>/dev/null | sed 's/.md//' | sort
grep -E "SUPPORTED_LIBRARIES|LIBRARIES" core/constants.py 2>/dev/null | head -5
```

## Run Test Suite

```bash
# Quick test run to check for failures
uv run pytest tests/unit -x -q --tb=no 2>/dev/null | tail -20
```

## Output Format

After analysis, provide a structured report:

### 1. Critical Issues (Must Fix)
Issues that could cause bugs, security problems, or break functionality.

### 2. High Priority (Should Fix)
Code smells, performance issues, or maintainability concerns.

### 3. Medium Priority (Consider)
Modernization opportunities, style improvements, minor inconsistencies.

### 4. Low Priority (Nice to Have)
Minor improvements, documentation updates, cosmetic changes.

### 5. Positive Patterns
Good practices found that should be maintained or expanded.

For each issue, provide:
- **Location**: File path and line number
- **Problem**: Clear description of the issue
- **Impact**: Why this matters
- **Solution**: Specific fix recommendation
- **Effort**: Low/Medium/High

## Exclusions

Do NOT flag:
- Plot implementations in `plots/` (AI-generated, different style rules)
- Generated files or lock files (`uv.lock`, `yarn.lock`, etc.)
- Third-party code
- Issues already tracked in pyproject.toml exclusions
