# Bug Planning

Create a new plan in specs/*.md to resolve the `Bug` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## GitHub Issue Detection

If the input below looks like a GitHub issue URL (e.g., `https://github.com/owner/repo/issues/123` or `#123`), you MUST:

1. **Fetch the issue** using: `gh issue view <number> --json title,body,comments,labels,author`
2. **Read all comments** to understand the full context, reproduction steps, and any clarifications
3. **Use the issue content** as the bug description instead of the raw URL
4. **Reference the issue** in the plan (e.g., "Fixes #123")

Example:
```bash
gh issue view 4150 --json title,body,comments,labels,author
```

## Instructions

- You're writing a plan to resolve a bug, it should be thorough and precise so we fix the root cause and prevent regressions.
- Create the plan in the `specs/*.md` file. Name it with format `YYMMDD-<descriptive-name>.md` (e.g., `250128-fix-database-connection.md`). Get the current date first.
- Use the plan format below to create the plan.
- Research the codebase to understand the bug, reproduce it, and put together a plan to fix it.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to fix the bug.
- Use your reasoning model: THINK HARD about the bug, its root cause, and the steps to fix it properly.
- IMPORTANT: Be surgical with your bug fix, solve the bug at hand and don't fall off track.
- IMPORTANT: We want the minimal number of changes that will fix and address the bug.
- Don't use decorators. Keep it simple.
- If you need a new library, use `uv add` and be sure to report it in the `Notes` section of the `Plan Format`.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `docs/ai_docs/project-guide.md` file.

## Relevant Files

Focus on the following files:
- `docs/ai_docs/project-guide.md` - Contains the project overview and development instructions.
- `api/**` - FastAPI backend (routers, schemas, dependencies).
- `core/**` - Shared business logic (database, repositories, config).
- `app/**` - React frontend (components, pages, hooks).
- `tests/**` - Test suite (unit, integration, e2e).
- `.github/workflows/**` - GitHub Actions workflows (CI/CD, automation).
- `automation/**` - Automation scripts.
- `docs/**` - Documentation.
- `plots/**` - Plot specifications and implementations (if relevant).
- `prompts/**` - AI agent prompts (if relevant).

## Plan Format

```md
# Bug: <bug name>

## Bug Description
<describe the bug in detail, including symptoms and expected vs actual behavior>

## Problem Statement
<clearly define the specific problem that needs to be solved>

## Solution Statement
<describe the proposed solution approach to fix the bug>

## Steps to Reproduce
<list exact steps to reproduce the bug>

## Root Cause Analysis
<analyze and explain the root cause of the bug>

## Relevant Files
Use these files to fix the bug:

<find and list the files that are relevant to the bug describe why they are relevant in bullet points. If there are new files that need to be created to fix the bug, list them in an h3 'New Files' section.>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers plus bullet points. use as many h3 headers as needed to fix the bug. Order matters, start with the foundational shared changes required to fix the bug then move on to the specific changes required to fix the bug. Include tests that will validate the bug is fixed with zero regressions. Your last step should be running the `Validation Commands` to validate the bug is fixed with zero regressions.>

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

<list commands you'll use to validate with 100% confidence the bug is fixed with zero regressions. every command must execute without errors so be specific about what you want to run to validate the bug is fixed with zero regressions. Include commands to reproduce the bug before and after the fix.>
- `uv run ruff check . && uv run ruff format .` - Lint and format code
- `uv run pytest tests/unit` - Run unit tests
- `uv run pytest tests/integration` - Run integration tests (if applicable)

## Notes
<optionally list any additional notes or context that are relevant to the bug that will be helpful to the developer>
```

## Bug
$ARGUMENTS
