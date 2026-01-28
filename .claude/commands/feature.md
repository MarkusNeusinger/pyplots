# Feature Planning

Create a new plan in specs/*.md to implement the `Feature` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## GitHub Issue Detection

If the input below looks like a GitHub issue URL (e.g., `https://github.com/owner/repo/issues/123` or `#123`), you MUST:

1. **Fetch the issue** using: `gh issue view <number> --json title,body,comments,labels,author`
2. **Read all comments** to understand the full context and any clarifications
3. **Use the issue content** as the feature description instead of the raw URL
4. **Reference the issue** in the plan (e.g., "Related to #123")

Example:
```bash
gh issue view 4150 --json title,body,comments,labels,author
```

## Instructions

- You're writing a plan to implement a net new feature that will add value to the application.
- Create the plan in the `specs/*.md` file. Name it with format `YYMMDD-<descriptive-name>.md` (e.g., `250128-add-user-auth.md`). Get the current date first.
- Use the `Plan Format` below to create the plan.
- Research the codebase to understand existing patterns, architecture, and conventions before planning the feature.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to implement the feature successfully.
- Use your reasoning model: THINK HARD about the feature requirements, design, and implementation approach.
- Follow existing patterns and conventions in the codebase. Don't reinvent the wheel.
- Design for extensibility and maintainability.
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
# Feature: <feature name>

## Feature Description
<describe the feature in detail, including its purpose and value to users>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<clearly define the specific problem or opportunity this feature addresses>

## Solution Statement
<describe the proposed solution approach and how it solves the problem>

## Relevant Files
Use these files to implement the feature:

<find and list the files that are relevant to the feature describe why they are relevant in bullet points. If there are new files that need to be created to implement the feature, list them in an h3 'New Files' section.>

## Implementation Plan
### Phase 1: Foundation
<describe the foundational work needed before implementing the main feature>

### Phase 2: Core Implementation
<describe the main implementation work for the feature>

### Phase 3: Integration
<describe how the feature will integrate with existing functionality>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers plus bullet points. use as many h3 headers as needed to implement the feature. Order matters, start with the foundational shared changes required then move on to the specific implementation. Include creating tests throughout the implementation process. Your last step should be running the `Validation Commands` to validate the feature works correctly with zero regressions.>

## Testing Strategy
### Unit Tests
<describe unit tests needed for the feature>

### Integration Tests
<describe integration tests needed for the feature>

### Edge Cases
<list edge cases that need to be tested>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

<list commands you'll use to validate with 100% confidence the feature is implemented correctly with zero regressions. every command must execute without errors so be specific about what you want to run to validate the feature works as expected. Include commands to test the feature end-to-end.>
- `uv run ruff check . && uv run ruff format .` - Lint and format code
- `uv run pytest tests/unit` - Run unit tests
- `uv run pytest tests/integration` - Run integration tests (if applicable)

## Notes
<optionally list any additional notes, future considerations, or context that are relevant to the feature that will be helpful to the developer>
```

## Feature
$ARGUMENTS
