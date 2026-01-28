# Chore Planning

Create a new plan in specs/*.md to resolve the `Chore` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## GitHub Issue Detection

If the input below looks like a GitHub issue URL (e.g., `https://github.com/owner/repo/issues/123` or `#123`), you MUST:

1. **Fetch the issue** using: `gh issue view <number> --json title,body,comments,labels,author`
2. **Read all comments** to understand the full context and any clarifications
3. **Use the issue content** as the chore description instead of the raw URL
4. **Reference the issue** in the plan (e.g., "Related to #123")

Example:
```bash
gh issue view 4150 --json title,body,comments,labels,author
```

## Instructions

- You're writing a plan to resolve a chore, it should be simple but we need to be thorough and precise so we don't miss anything or waste time with any second round of changes.
- Create the plan in the `specs/*.md` file. Name it with format `YYMMDD-<descriptive-name>.md` (e.g., `250128-update-dependencies.md`). Get the current date first.
- Use the plan format below to create the plan.
- Research the codebase and put together a plan to accomplish the chore.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to accomplish the chore.
- Use your reasoning model: THINK HARD about the plan and the steps to accomplish the chore.
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
# Chore: <chore name>

## Chore Description
<describe the chore in detail>

## Relevant Files
Use these files to resolve the chore:

<find and list the files that are relevant to the chore describe why they are relevant in bullet points. If there are new files that need to be created to accomplish the chore, list them in an h3 'New Files' section.>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers plus bullet points. use as many h3 headers as needed to accomplish the chore. Order matters, start with the foundational shared changes required to fix the chore then move on to the specific changes required to fix the chore. Your last step should be running the `Validation Commands` to validate the chore is complete with zero regressions.>

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

<list commands you'll use to validate with 100% confidence the chore is complete with zero regressions. every command must execute without errors so be specific about what you want to run to validate the chore is complete with zero regressions. Don't validate with curl commands.>
- `uv run ruff check . && uv run ruff format .` - Lint and format code
- `uv run pytest tests/unit` - Run unit tests
- `uv run pytest tests/integration` - Run integration tests (if applicable)

## Final Check
- Use `mcp__plugin_serena_serena__think_about_whether_you_are_done` to verify all tasks are complete.

## Notes
<optionally list any additional notes or context that are relevant to the chore that will be helpful to the developer>
```

## Chore
$ARGUMENTS
