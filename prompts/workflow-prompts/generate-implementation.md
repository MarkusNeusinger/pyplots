# Generate Library Implementation

Generate a **${LIBRARY}** implementation for the plot specification `${SPEC_ID}`.

## Instructions

You are generating ONLY the **${LIBRARY}** implementation. Focus exclusively on this library.

### Step 1: Read Required Files

1. `prompts/plot-generator.md` - Base generation rules
2. `prompts/quality-criteria.md` - Quality requirements
3. `prompts/library/${LIBRARY}.md` - Library-specific rules
4. `specs/${SPEC_ID}.md` - The specification

### Step 2: Check for Previous Attempts

${PREVIOUS_ATTEMPTS_CONTEXT}

### Step 3: Generate Implementation

Create the implementation file at the correct path:
```
plots/${LIBRARY}/{plot_type}/${SPEC_ID}/default.py
```

Determine `{plot_type}` from the spec (e.g., scatter, bar, line, heatmap).

### Step 4: Test the Implementation

Run the implementation to verify it works:
```bash
source .venv/bin/activate
MPLBACKEND=Agg python plots/${LIBRARY}/{plot_type}/${SPEC_ID}/default.py
```

### Step 5: Create PR

Only if the implementation is successful:

- **Branch:** `auto/${SPEC_ID}/${LIBRARY}`
- **Title:** `feat(${LIBRARY}): implement ${SPEC_ID}`
- **Body:**
```markdown
## Summary
Implements `${SPEC_ID}` for **${LIBRARY}** library.

**Parent Issue:** #${MAIN_ISSUE_NUMBER}
**Sub-Issue:** #${SUB_ISSUE_NUMBER}
**Attempt:** ${ATTEMPT}/3

## Implementation
- `plots/${LIBRARY}/{plot_type}/${SPEC_ID}/default.py`
```

## Important Notes

- Focus ONLY on ${LIBRARY} - do not generate code for other libraries
- If you cannot implement this plot type in ${LIBRARY}, explain why in the PR body
- Document any limitations or workarounds in code comments
