# Task Classification

Classify the task description into exactly one category.

## Task

$ARGUMENTS

## Rules

Analyze the task and classify it:

- `bug` — Something is broken, errors occur, regressions, 404s, crashes, incorrect behavior, things that used to work
- `feature` — New functionality, additions, enhancements, new pages, new endpoints, new capabilities
- `chore` — Maintenance, cleanup, config changes, dependency updates, documentation, CI/CD, formatting
- `refactor` — Restructuring code while preserving behavior: extracting modules, reorganizing files, splitting classes, renaming for clarity, moving code between files

## Response

Respond with ONLY a JSON object on a single line. No explanation, no markdown, no code fences:

{"type": "bug", "reason": "one sentence explaining why"}
