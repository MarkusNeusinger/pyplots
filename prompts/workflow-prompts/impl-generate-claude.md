# Generate Implementation

**YOUR PRIMARY TASK: Create a working Python plot implementation file.**

You MUST create: `plots/{SPEC_ID}/implementations/{LIBRARY}.py`

This is NOT optional. The workflow will FAIL if this file does not exist after you finish.

---

**Variables:**
- LIBRARY: {LIBRARY}
- SPEC_ID: {SPEC_ID}
- Regeneration: {IS_REGENERATION}

## Step 1: Read the rules (quickly)

Read these files to understand the requirements:

1. `prompts/plot-generator.md` - Base generation rules
2. `prompts/library/{LIBRARY}.md` - Library-specific rules (CRITICAL!)
3. `plots/{SPEC_ID}/specification.md` - What to visualize

Optional (if regenerating):
- `plots/{SPEC_ID}/metadata/{LIBRARY}.yaml` - Previous review feedback
- `plots/{SPEC_ID}/implementations/{LIBRARY}.py` - Previous implementation

## Step 2: CREATE THE FILE (MANDATORY)

**You MUST use the Write tool to create:**

```
plots/{SPEC_ID}/implementations/{LIBRARY}.py
```

The script MUST:
- Follow the KISS structure: imports → data → plot → save
- Save output as `plot.png` in current directory
- For interactive libraries (plotly, bokeh, altair, highcharts, pygal, letsplot): also save `plot.html`

**DO NOT SKIP THIS STEP. The file MUST be created.**

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

## Step 6: Verify file exists (CRITICAL)

Before committing, verify the implementation file exists:

```bash
ls -la plots/{SPEC_ID}/implementations/{LIBRARY}.py
```

**If the file does NOT exist, you MUST go back to Step 2 and create it!**

## Step 7: Commit

```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add plots/{SPEC_ID}/implementations/{LIBRARY}.py
git commit -m "feat({LIBRARY}): implement {SPEC_ID}"
git push -u origin implementation/{SPEC_ID}/{LIBRARY}
```

## Final Check

Before finishing, confirm:
1. ✅ `plots/{SPEC_ID}/implementations/{LIBRARY}.py` exists
2. ✅ `plot.png` was generated successfully
3. ✅ Changes were committed and pushed

If any of these failed, DO NOT report success.
