# AI Quality Review

Evaluate if the **${LIBRARY}** implementation matches the specification for `${SPEC_ID}`.

## Context

- **Spec ID:** ${SPEC_ID}
- **Library:** ${LIBRARY}
- **PR Number:** #${PR_NUMBER}
- **Sub-Issue:** #${SUB_ISSUE_NUMBER}
- **Attempt:** ${ATTEMPT}/3

## Your Task

### 1. Read the Spec File
`plots/${SPEC_ID}/spec.md`
- Note all quality criteria listed
- Understand the expected visual output

### 2. Read the Implementation
`plots/${SPEC_ID}/implementations/${LIBRARY}.py`

### 3. Read Library-Specific Rules
`prompts/library/${LIBRARY}.md`

### 4. View Plot Images
Check the `plot_images/` directory
- Use your vision capabilities to analyze each image
- Compare with the spec requirements

### 5. Evaluate Against Quality Criteria
Read `prompts/quality-criteria.md`

### 6. Post Verdict to Sub-Issue #${SUB_ISSUE_NUMBER}

Use this EXACT format:

```markdown
## AI Review - Attempt ${ATTEMPT}/3

### Quality Evaluation
| Evaluator | Score | Verdict |
|-----------|-------|---------|
| Claude | XX/100 | approve/reject |

### Criteria Checklist
- [x] VQ-001: Axes labeled correctly
- [x] VQ-002: Grid is subtle
- [ ] VQ-003: Elements clear ← Issue here
- [x] CQ-001: Type hints present
...

### Issues Found
1. **VQ-003 FAILED**: Legend overlaps with data points
2. **CQ-002 PARTIAL**: Docstring missing return type

### AI Feedback for Next Attempt
> Move legend outside plot area with `bbox_to_anchor=(1.05, 1)`
> Add return type to docstring

### Verdict: APPROVED / REJECTED
```

### 7. Take Action Based on Result

**APPROVED** (score >= 85):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-approved
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-approved
```

**REJECTED** (score < 85):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-rejected
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-rejected
```

## Important

- This is a **${LIBRARY}-only** review - focus only on this library
- Post feedback to **Sub-Issue #${SUB_ISSUE_NUMBER}**, NOT the main issue
- Include the generated code in your review comment for documentation
