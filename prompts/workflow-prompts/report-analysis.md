# Report Analysis Prompt

Analyzes user-submitted issue reports and provides structured feedback.

## Task

Validate and structure a user-submitted issue report for an existing plot specification or implementation.

## Input

From the issue body, extract:
- **spec_id**: The specification ID (e.g., `scatter-basic`, `qrcode-basic`)
- **target**: "Specification" or "Implementation"
- **library**: The library name (if implementation issue)
- **category**: Visual, Data, Functional, or Other
- **description**: User's description of the issue

## Validation Steps

1. **Verify spec exists:**
   ```bash
   ls plots/{spec_id}/
   ```
   If not found → post comment, close issue, STOP

2. **If implementation issue, verify library exists:**
   ```bash
   ls plots/{spec_id}/implementations/{library}.py
   ```
   If not found → post comment, close issue, STOP

3. **Read relevant files:**
   - `plots/{spec_id}/specification.md`
   - `plots/{spec_id}/metadata/{library}.yaml` (if impl)

4. **Analyze the issue:**
   - Is this a legitimate issue or misunderstanding?
   - Does the described problem match what's in the spec/metadata?
   - What might be the root cause?

## Output Format

Post a comment with this structure:

```markdown
## Report Analysis

**Specification:** `{spec_id}`
**Target:** {Specification / Implementation ({library})}
**Category:** {Visual / Data / Functional / Other}

### Problem Summary
{AI-structured version of the user's description - clear, concise, 2-3 sentences}

### Analysis
{Assessment of the issue:
- Is this a valid issue?
- What might be causing it?
- Brief technical insight if applicable}

### Recommended Action
- **Spec update needed:** {Yes/No} - {brief reason}
- **Regeneration needed:** {Yes/No} - {which libraries if yes}

---
**Next:** Add `approved` label when ready to fix.
```

## Label Updates

After posting the comment, update labels:

1. **Remove:** `report-pending`
2. **Add:** `report-validated`
3. **Add target label:**
   - For spec issues: `report:spec`
   - For impl issues: `report:impl` AND `report:impl:{library}`
4. **Add category label:**
   - Visual → `category:visual`
   - Data → `category:data`
   - Functional → `category:functional`
   - Other → `category:other`

## Title Update

Update the issue title to include the spec ID:
```bash
gh issue edit {number} --title "[{spec_id}] {brief description of the issue}"
```

Keep the description under 60 characters.

## Important Notes

- Do NOT add the `approved` label
- Do NOT trigger any fix workflows
- Keep analysis concise but informative
- Be objective - some reports may be user misunderstandings
- If the issue is unclear, ask for clarification instead of closing
