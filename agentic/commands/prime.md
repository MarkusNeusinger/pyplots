# Prime

> Execute the following sections to understand the codebase then summarize your understanding.

## Run

```bash
# Current state: branch, uncommitted changes, stashes
git status --short --branch

# Recent activity: what's been worked on
git log --oneline --graph -15

# Open PRs: what's in flight
gh pr list --limit 10 2>/dev/null || echo "(gh CLI not available)"
```

## Read

@agentic/docs/project-guide.md
@agentic/commands/context.md
@docs/concepts/vision.md
@pyproject.toml

## Serena

- Run `activate_project` with project "pyplots"
- Run `list_memories` and read relevant ones
- Run `check_onboarding_performed`

Prefer Serena's symbolic tools (`jet_brains_find_symbol`, `jet_brains_get_symbols_overview`,
`jet_brains_find_referencing_symbols`) over brute-force file scanning.

Use Serena's thinking tools to maintain focus:

- `think_about_collected_information` - after research/search sequences
- `think_about_task_adherence` - before making code changes
- `think_about_whether_you_are_done` - when task seems complete
