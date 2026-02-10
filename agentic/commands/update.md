# Update Implementation

> Local interactive workflow for updating plot implementations. Spawns per-library Opus agents that modify, regenerate,
> and preview plots in parallel. The lead coordinates iteration based on user feedback and handles shipping (GCS upload,
> git branch, PR, review trigger).

## Context

@CLAUDE.md
@pyproject.toml

## Instructions

You are the **update-lead**. Your job is to coordinate a team of per-library updater agents, present results to the
user, iterate on feedback, and ship the final changes.

**Prerequisite**: This command uses agent teams (experimental). Ensure `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
in your environment or Claude Code settings.

---

### Phase 1: Parse & Setup

Parse `$ARGUMENTS` using this format:

```
/update {spec-id} [{libraries}] [{description}]
/update {issue-url-or-number}
```

**Argument parsing rules:**

1. **Issue URL or `#N` number**: If the first argument is a GitHub URL containing `/issues/` or starts with `#`, run
   `gh issue view {number} --json title,body,labels` to extract:
    - `spec_id`: from issue body or labels (look for `spec:` label prefix or spec-id mention)
    - `libraries`: from issue body or labels (look for `impl:` label prefix or library mentions)
    - `description`: from issue title and body
2. **Normal arguments**: First arg is `spec_id`. Second arg (if comma-separated list of known libraries) is the library
   filter. Everything after is the `description`.
3. **Known libraries**: `matplotlib`, `seaborn`, `plotly`, `bokeh`, `altair`, `plotnine`, `pygal`, `highcharts`,
   `letsplot`
4. **Default libraries**: If no libraries specified, scan `plots/{spec_id}/implementations/` for existing `*.py` files (
   excluding `__init__.py`) — update all that exist.

**Validation:**

- Confirm `plots/{spec_id}/` exists (abort with helpful message if not)
- Confirm `plots/{spec_id}/specification.md` exists
- Confirm at least one implementation exists for the requested libraries
- List which libraries will be updated and ask user to confirm before proceeding

**Read specification once**: Read `plots/{spec_id}/specification.md` — you'll pass context to agents.

---

### Phase 2: Create Team & Spawn Agents

1. **Create team**: `TeamCreate` with name `update-{spec_id}`

2. **Create one task per library**: Use `TaskCreate` with:
    - Subject: `Update {library} implementation for {spec_id}`
    - Description: Include spec_id, library, and the user's description

3. **Spawn one `general-purpose` opus agent per library** via `Task` tool with:
    - `team_name`: `update-{spec_id}`
    - `name`: `{library}-updater`
    - `subagent_type`: `general-purpose`
    - `model`: `opus`
    - The **library-updater prompt** (see below), with `{SPEC_ID}`, `{LIBRARY}`, and `{DESCRIPTION}` filled in

4. **Assign tasks** to the corresponding agents via `TaskUpdate`

All agents run in parallel — each only touches its own library's files.

---

### Phase 3: Collect & Present

Agents report back via `SendMessage` (auto-delivered to you). Agents may report either **completed work** (`STATUS: done`) or **a conflict** (`STATUS: conflict`). Once all agents have reported:

1. **Handle conflicts first.** If any agent reports a conflict:
   - Present the conflict to the user clearly: which rule/spec is violated, what the agent suggests as alternatives
   - Ask the user to decide:
     - **Adjust the request** to comply with existing rules
     - **Update the rule or spec** — the user tells you which file to edit and how, you make the edit, then tell the agent to proceed
     - **Override** — explicitly tell the agent to proceed despite the conflict
   - Send the user's decision to the agent via `SendMessage`. The agent will then continue with Step 3.

2. **Present a summary to the user** for each library that completed successfully:
   - What was changed (bullet points from agent)
   - Local preview image path: `plots/{spec_id}/implementations/.update-preview/{library}/plot.png`
   - Agent's self-assessment score
   - Any spec changes the agent made

3. **Ask the user for feedback.** They can:
   - Give per-library feedback (e.g., "matplotlib looks good, seaborn needs more contrast")
   - Say **"ship"**, **"ok"**, **"looks good"**, or **"passt"** to proceed to shipping
   - Say **"abort"** to cancel everything

---

### Phase 4: Iterate

For per-library feedback:

1. Send the feedback to the specific idle teammate via `SendMessage` (e.g., to `seaborn-updater`). This wakes them up.
2. The agent runs its conflict check again (Step 2) on the new feedback. If it detects a conflict, it reports back with `STATUS: conflict` instead of making changes — handle as in Phase 3.
3. If no conflict, the agent re-modifies, re-generates, reports back, and goes idle again.
4. Present updated results to the user.
5. Repeat until the user approves.

---

### Phase 5: Ship

**Only proceed when the user explicitly approves shipping.**

The lead handles all shipping directly (no delegation to teammates):

#### 5a. Code Quality

```bash
uv run ruff format plots/{spec_id}/implementations/*.py
uv run ruff check --fix plots/{spec_id}/implementations/*.py
```

#### 5b. Update Metadata YAML

For each updated library, edit `plots/{spec_id}/metadata/{library}.yaml`:

| Field             | Value                                                                     |
|-------------------|---------------------------------------------------------------------------|
| `updated`         | Current UTC timestamp in ISO 8601 (e.g., `2026-02-10T14:30:00+00:00`)     |
| `generated_by`    | Get from `CLAUDE_MODEL` env var, or detect via `claude --version` / model name |
| `python_version`  | Get from `uv run python --version`                                        |
| `library_version` | Get from `uv run python -c "from importlib.metadata import version; print(version('{package}'))"` where `{package}` is the pip package name. Mapping: `highcharts` → `highcharts-core`, `letsplot` → `lets-plot`, all others → same as `{library}` |
| `quality_score`   | Set to `null` (CI review will fill this)                                  |
| All other fields  | **Keep unchanged** (including `review`, `impl_tags`, `preview_url`, etc.) |

#### 5c. Update Implementation Header

For each updated library, ensure the implementation file starts with:

```python
""" pyplots.ai
{spec_id}: {Title from specification}
Library: {library} {lib_version} | Python {py_version}
Quality: /100 | Updated: {YYYY-MM-DD}
"""
```

#### 5d. Copy Final Images

For each library, copy the preview images to the implementations directory for GCS upload:

```bash
cp plots/{spec_id}/implementations/.update-preview/{library}/plot.png plots/{spec_id}/implementations/plot.png
# Process images (thumbnail + optimization)
uv run python -m core.images process \
  plots/{spec_id}/implementations/plot.png \
  plots/{spec_id}/implementations/plot.png \
  plots/{spec_id}/implementations/plot_thumb.png
```

Note: Since we process one library at a time for GCS upload, handle sequentially.

#### 5e. GCS Staging Upload

For each library:

```bash
STAGING_PATH="gs://pyplots-images/staging/{spec_id}/{library}"

# Upload PNG
gsutil cp plots/{spec_id}/implementations/plot.png "${STAGING_PATH}/plot.png"
gsutil acl ch -u AllUsers:R "${STAGING_PATH}/plot.png" 2>/dev/null || true

# Upload thumbnail
gsutil cp plots/{spec_id}/implementations/plot_thumb.png "${STAGING_PATH}/plot_thumb.png"
gsutil acl ch -u AllUsers:R "${STAGING_PATH}/plot_thumb.png" 2>/dev/null || true

# Upload HTML if it exists (interactive libraries: plotly, bokeh, altair, highcharts, pygal, letsplot)
if [ -f "plots/{spec_id}/implementations/.update-preview/{library}/plot.html" ]; then
  gsutil cp "plots/{spec_id}/implementations/.update-preview/{library}/plot.html" "${STAGING_PATH}/plot.html"
  gsutil acl ch -u AllUsers:R "${STAGING_PATH}/plot.html" 2>/dev/null || true
fi
```

Update `preview_url` and `preview_thumb` in the metadata YAML to point to the staging URLs:

- `preview_url`: `https://storage.googleapis.com/pyplots-images/staging/{spec_id}/{library}/plot.png`
- `preview_thumb`: `https://storage.googleapis.com/pyplots-images/staging/{spec_id}/{library}/plot_thumb.png`

#### 5f. Clean Up Preview Directory

```bash
rm -rf plots/{spec_id}/implementations/.update-preview
```

#### 5g. Per-Library Branches, PRs & Reviews

**IMPORTANT:** The review pipeline (`impl-review.yml`) extracts `SPEC_ID` and `LIBRARY` from the branch name
pattern `implementation/{spec-id}/{library}`. Therefore, each library MUST get its own branch and PR.

Get `{owner}/{repo}` from `git remote get-url origin`.

**If the spec was changed**, commit that first on main or include it in each branch.

**For each library**, run the following sequentially:

```bash
# Ensure we start from main
git checkout main

# Create per-library branch
git checkout -b implementation/{spec_id}/{library}

# Stage only this library's files
git add plots/{spec_id}/implementations/{library}.py
git add plots/{spec_id}/metadata/{library}.yaml
# If spec was changed (only needed in first library branch):
git add plots/{spec_id}/specification.md

# Commit
git commit -m "update({spec_id}): {library} — {short description}

{description}"

# Push
git push -u origin implementation/{spec_id}/{library}

# Create PR
gh pr create \
  --title "update({spec_id}): {library} — {short description}" \
  --body "$(cat <<EOF
## Summary

Updated **{library}** implementation for **{spec_id}**.

**Changes:** {description}

### Changes
{bullet points of changes from agent}
- Quality self-assessment: {score}/100

## Test Plan

- [x] Preview images uploaded to GCS staging
- [x] Implementation file passes ruff format/check
- [x] Metadata YAML updated with current versions
- [ ] Automated review triggered

---
Generated with [Claude Code](https://claude.com/claude-code) \`/update\` command
EOF
)"

# Trigger review for this PR
PR_NUMBER=$(gh pr view --json number -q '.number')
gh api repos/{owner}/{repo}/dispatches \
  -f event_type=review-pr \
  -f 'client_payload[pr_number]='"$PR_NUMBER"
```

After all branches are created, return to main:

```bash
git checkout main
```

Report all PR URLs to the user.

#### 5j. Cleanup Team

1. `SendMessage` with type `shutdown_request` to all agents
2. `TeamDelete` to clean up the team
3. Report all PR URLs to the user

---

## Library-Updater Agent Prompt

Use this prompt when spawning each per-library agent. Replace `{SPEC_ID}`, `{LIBRARY}`, and `{DESCRIPTION}` with actual
values.

---

You are the **{LIBRARY}-updater** on the `update-{SPEC_ID}` team. Your job is to update the {LIBRARY} implementation for
**{SPEC_ID}**.

**Task:** {DESCRIPTION}

### Step 1: Read Context

Read these files to understand what you're working with:

1. `plots/{SPEC_ID}/specification.md` — the specification (what the plot should show)
2. `plots/{SPEC_ID}/implementations/{LIBRARY}.py` — current implementation to update
3. `plots/{SPEC_ID}/metadata/{LIBRARY}.yaml` — review feedback from last review:
    - `review.strengths` — PRESERVE these (don't break what works)
    - `review.weaknesses` — FIX these
    - `review.criteria_checklist` — items with `passed: false` need fixing
    - `quality_score` — current score to beat
4. `prompts/library/{LIBRARY}.md` — library-specific rules (**CRITICAL**: follow these exactly)
5. `prompts/plot-generator.md` — base generation rules
6. `prompts/quality-criteria.md` — quality scoring criteria

If `preview_url` exists in the metadata, view the current preview image to understand what the plot currently looks
like.

### Step 2: Conflict Check

**Before making any changes**, check whether the user's request conflicts with:
- **Generation rules** (`prompts/plot-generator.md`, `prompts/library/{LIBRARY}.md`)
- **Quality criteria** (`prompts/quality-criteria.md`)
- **The specification** (`plots/{SPEC_ID}/specification.md`)

If you detect a conflict, **DO NOT proceed with the change.** Instead, report the conflict to `update-lead` via `SendMessage`:

```
LIBRARY: {LIBRARY}
STATUS: conflict

CONFLICT:
The requested change "{specific request}" conflicts with:
- {rule source}: {quote the specific rule}
- Reason: {explain why this is a conflict}

OPTIONS:
1. Adjust the request to: {suggest a compliant alternative}
2. Update the rule/spec to allow this (user must decide)
3. Proceed anyway (user must explicitly override)
```

Then go idle and wait for the lead to relay the user's decision. Only proceed once the conflict is resolved.

### Step 3: Modify Implementation

Edit `plots/{SPEC_ID}/implementations/{LIBRARY}.py`:

- Follow all rules from `prompts/plot-generator.md` and `prompts/library/{LIBRARY}.md`
- KISS structure: imports → data → plot → save
- Preserve review strengths, fix weaknesses
- Address the user's specific request: **{DESCRIPTION}**
- If no specific request was given, focus on fixing review weaknesses and improving quality score

If the specification itself needs changes to make the plot better, also edit `plots/{SPEC_ID}/specification.md` and
explain what you changed and why.

### Step 4: Generate Locally

Run the implementation to generate the plot image. **IMPORTANT**: Each agent MUST run in its own isolated preview
directory to avoid race conditions with other parallel agents. All agents write `plot.png` — running in the shared
`implementations/` directory causes file conflicts.

```bash
mkdir -p plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}
cd plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY} && MPLBACKEND=Agg uv run python ../../{LIBRARY}.py
```

This runs `{LIBRARY}.py` from the isolated `.update-preview/{LIBRARY}/` directory, so `plot.png` and `plot.html` land
there directly — no copy step needed, no race condition with other agents.

If the script fails, read the error, fix the implementation, and retry. **Up to 3 retries.**

### Step 5: Process Images

Generate thumbnail and optimize:

```bash
uv run python -m core.images process \
  plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}/plot.png \
  plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}/plot.png \
  plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}/plot_thumb.png
```

### Step 6: Self-Check

View the generated image at `plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}/plot.png`.

Check against the quality criteria from `prompts/quality-criteria.md`:

- Text legibility (title 24pt, labels 20pt, ticks 16pt)
- No overlapping elements
- Elements visible and distinguishable
- Color accessibility
- Layout balance (16:9)
- Correct axis labels with units
- Spec compliance

Fix any obvious issues before reporting.

### Step 7: Report to Lead

Send a message to `update-lead` via `SendMessage` with:

```
LIBRARY: {LIBRARY}
STATUS: done

CHANGES:
- {bullet point 1}
- {bullet point 2}
- ...

IMAGE: plots/{SPEC_ID}/implementations/.update-preview/{LIBRARY}/plot.png
SELF_SCORE: {your estimated quality score}/100

SPEC_CHANGES: {none, or describe what you changed in specification.md}

ISSUES: {none, or describe any problems encountered}
```

Then mark your task as completed via `TaskUpdate`.

**After reporting, go idle. The lead will wake you if the user has feedback for revisions.**

If the lead sends you feedback, repeat Steps 2-7 with the new instructions (including the conflict check).

---

## Usage Examples

```
# Update all existing implementations for a spec (no description)
/update area-basic

# Update single library
/update area-basic matplotlib

# Update specific libraries with description
/update area-basic matplotlib,seaborn fix the axis label overlap

# Update from a GitHub issue
/update #3970
/update https://github.com/MarkusNeusinger/pyplots/issues/3970
```
