# Generate Implementation

You are generating the **{LIBRARY}** implementation for **{SPEC_ID}**.

**Regeneration:** {IS_REGENERATION}

## Step 1: Read required files

1. `prompts/plot-generator.md` - Base generation rules (IMPORTANT: Read the "Regeneration" section!)
2. `prompts/default-style-guide.md` - Visual style requirements
3. `prompts/quality-criteria.md` - Quality requirements
4. `prompts/library/{LIBRARY}.md` - Library-specific rules
5. `plots/{SPEC_ID}/specification.md` - The specification

## Step 1b: If Regeneration, read previous feedback

If this is a regeneration ({IS_REGENERATION} == true):

1. Read `plots/{SPEC_ID}/metadata/{LIBRARY}.yaml`
   - Look at `review.strengths` (keep these aspects!)
   - Look at `review.weaknesses` (fix these problems - decide HOW yourself)
   - Look at `review.image_description` (understand what was generated visually)
   - Look at `review.criteria_checklist` (see exactly which criteria failed)
     - Focus on categories with low scores (e.g., visual_quality.score < visual_quality.max)
     - Check items with `passed: false` - these need fixing
     - VQ-XX items for visual issues
     - SC-XX items for spec compliance
     - CQ-XX items for code quality
2. Read `plots/{SPEC_ID}/implementations/{LIBRARY}.py`
   - Understand what was done before
   - Keep what worked, fix what didn't

## Step 2: Generate implementation

Create: `plots/{SPEC_ID}/implementations/{LIBRARY}.py`

The script MUST:
- Save as `plot.png` in the current directory
- For interactive libraries (plotly, bokeh, altair, highcharts, pygal, letsplot): also save `plot.html`

## Step 3: Test and fix (up to 3 attempts)

Run the implementation:
```bash
source .venv/bin/activate
cd plots/{SPEC_ID}/implementations
MPLBACKEND=Agg python {LIBRARY}.py
```

If it fails, fix and try again (max 3 attempts).

## Step 4: Visual self-check

Look at the generated `plot.png`:
- Does it match the specification?
- Are axes labeled correctly?
- Is the visualization clear?

## Step 5: Format the code

```bash
source .venv/bin/activate
ruff format plots/{SPEC_ID}/implementations/{LIBRARY}.py
ruff check --fix plots/{SPEC_ID}/implementations/{LIBRARY}.py
```

## Step 6: Commit

```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add plots/{SPEC_ID}/implementations/{LIBRARY}.py
git commit -m "feat({LIBRARY}): implement {SPEC_ID}"
git push -u origin implementation/{SPEC_ID}/{LIBRARY}
```

## Report result

Print exactly one line:
- `GENERATION_SUCCESS` - if everything worked
- `GENERATION_FAILED: <reason>` - if it failed
