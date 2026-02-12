# Repair Implementation

You are repairing the **{LIBRARY}** implementation for **{SPEC_ID}**.

This is **repair attempt {ATTEMPT}/3**. The previous implementation was rejected.

## Step 1: Read the AI review feedback

Read both sources to understand what needs to be fixed:

1. `/tmp/ai_feedback.md` - Full review from PR comments
2. `plots/{SPEC_ID}/metadata/{LIBRARY}.yaml` - Look at:
   - `review.strengths` (keep these aspects!)
   - `review.weaknesses` (fix these problems - decide HOW yourself)
   - `review.image_description` (understand what was generated visually)
   - `review.criteria_checklist` (see exactly which criteria failed)
     - Look for items with `passed: false` - these need fixing
     - Focus on categories with low scores (e.g., visual_quality.score < visual_quality.max)
     - VQ-XX items for visual issues
     - SC-XX items for spec compliance
     - CQ-XX items for code quality

**Important:** If the review triggered AR-08 (FAKE_FUNCTIONALITY), this is NOT repairable via repair. The implementation must either be regenerated as a genuine static visualization or marked NOT_FEASIBLE. Do NOT fix by "improving" the fake elements.

## Step 2: Read reference files

1. `prompts/library/{LIBRARY}.md` - Library-specific rules
2. `plots/{SPEC_ID}/specification.md` - The specification
3. `prompts/quality-criteria.md` - Quality requirements

## Step 3: Read current implementation

`plots/{SPEC_ID}/implementations/{LIBRARY}.py`

## Step 4: Fix the issues

Based on the AI feedback, fix:
- Visual quality issues
- Code quality issues
- Spec compliance issues

## Step 5: Test the fix

```bash
source .venv/bin/activate
cd plots/{SPEC_ID}/implementations
MPLBACKEND=Agg python {LIBRARY}.py
```

## Step 6: Visual self-check

View `plot.png` and verify fixes are correct.

## Step 7: Format the code

```bash
source .venv/bin/activate
ruff format plots/{SPEC_ID}/implementations/{LIBRARY}.py
ruff check --fix plots/{SPEC_ID}/implementations/{LIBRARY}.py
```

## Step 8: Commit and push

```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add plots/{SPEC_ID}/implementations/{LIBRARY}.py
git commit -m "fix({LIBRARY}): address review feedback for {SPEC_ID}

Attempt {ATTEMPT}/3 - fixes based on AI review"
git push origin {BRANCH}
```

## Report result

Print: `REPAIR_SUCCESS` or `REPAIR_FAILED: <reason>`
