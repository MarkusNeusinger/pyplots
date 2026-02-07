# Commit

Follow the `Instructions` below to create a git commit with a properly formatted conventional commit message.

## Variables

run_id: $1
task_type: $2

## Instructions

- Generate a concise commit message using conventional commit format: `<type>: <message>`
- The `<type>` should match the task_type variable if provided, mapped as follows:
  - `feature` → `feat`
  - `bug` → `fix`
  - `chore` → `chore`
  - `refactor` → `refactor`
  - If no task_type is provided, infer the type from the changes
- The `<message>` should be:
  - Present tense (e.g., "add", "fix", "update", not "added", "fixed", "updated")
  - 72 characters or less for the first line
  - Descriptive of the actual changes made
  - No period at the end
  - Lowercase start
- Examples:
  - `feat: add CSV export to API endpoints`
  - `fix: resolve 404 error on /api/plots`
  - `chore: update dependencies to latest versions`
  - `refactor: simplify JSON parsing logic`

## Run

1. Run `git diff HEAD` to understand what changes have been made
2. Run `git status` to see which files are modified/untracked
3. Stage changes with `git add` — prefer adding specific files over `git add -A`
4. Run `git commit -m "<generated_commit_message>"` to create the commit

## Report

Return ONLY the commit message that was used (no other text).
