# AI Quality Review

Evaluate if the **${LIBRARY}** implementation matches the specification for `${SPEC_ID}`.

## Context

- **Spec ID:** ${SPEC_ID}
- **Library:** ${LIBRARY}
- **PR Number:** #${PR_NUMBER}
- **Sub-Issue:** #${SUB_ISSUE_NUMBER}
- **Attempt:** ${ATTEMPT}/3

## Your Task

### 1. Read the Specification
`plots/${SPEC_ID}/specification.md`
- Understand what the plot should show
- Note all required features

### 2. Read the Implementation
`plots/${SPEC_ID}/implementations/${LIBRARY}.py`

### 3. Read Library-Specific Rules
`prompts/library/${LIBRARY}.md`

### 4. View the Generated Plot
Check the `plot_images/` directory
- Use your vision capabilities to analyze the image
- Compare with the spec requirements

### 5. Evaluate Using 3-Area Criteria

Read `prompts/quality-criteria.md` and evaluate:

#### Spec Compliance (40 pts)
| ID | Criterion | Pts | Check |
|----|-----------|-----|-------|
| SC-01 | Plot Type | 12 | Correct chart type? |
| SC-02 | Data Mapping | 8 | X/Y correct? |
| SC-03 | Required Features | 8 | All features from spec? |
| SC-04 | Data Range | 4 | Axis ranges appropriate? |
| SC-05 | Legend Accuracy | 4 | Labels match data? |
| SC-06 | Title Format | 4 | `{spec-id} · {library} · pyplots.ai`? |

#### Visual Quality (40 pts)
| ID | Criterion | Pts | Check |
|----|-----------|-----|-------|
| VQ-01 | Axis Labels | 8 | Meaningful labels? |
| VQ-02 | No Overlap | 7 | Text readable? |
| VQ-03 | Color Choice | 6 | Colorblind-safe? |
| VQ-04 | Element Clarity | 6 | Points/bars visible? |
| VQ-05 | Layout Balance | 5 | No cut-off content? |
| VQ-06 | Grid Subtlety | 3 | Grid subtle? |
| VQ-07 | Legend Placement | 3 | Doesn't cover data? |
| VQ-08 | Image Size | 2 | 4800x2700 px? |

#### Code Quality (20 pts)
| ID | Criterion | Pts | Check |
|----|-----------|-----|-------|
| CQ-01 | KISS Structure | 5 | No functions/classes? |
| CQ-02 | Reproducibility | 4 | Seed or deterministic? |
| CQ-03 | Library Idioms | 4 | Best practices? |
| CQ-04 | Clean Imports | 2 | Only used imports? |
| CQ-05 | Helpful Comments | 2 | Non-obvious explained? |
| CQ-06 | No Deprecated API | 2 | Current functions? |
| CQ-07 | Output Correct | 1 | Saves as plot.png? |

### 6. Post Verdict to Sub-Issue #${SUB_ISSUE_NUMBER}

Use this EXACT format:

```markdown
## AI Review - Attempt ${ATTEMPT}/3

### Score: XX/100

| Area | Score | Max |
|------|-------|-----|
| Spec Compliance | XX | 40 |
| Visual Quality | XX | 40 |
| Code Quality | XX | 20 |
| **Total** | **XX** | **100** |

### Spec Compliance (XX/40)
- [x] SC-01: Plot Type (12)
- [x] SC-02: Data Mapping (8)
- [x] SC-03: Required Features (8)
- [x] SC-04: Data Range (4)
- [ ] SC-05: Legend Accuracy (4) - N/A
- [x] SC-06: Title Format (4)

### Visual Quality (XX/40)
- [x] VQ-01: Axis Labels (8)
- [x] VQ-02: No Overlap (7)
- [ ] VQ-03: Color Choice (6) - Red-green combination
- [x] VQ-04: Element Clarity (6)
- [x] VQ-05: Layout Balance (5)
- [x] VQ-06: Grid Subtlety (3)
- [x] VQ-07: Legend Placement (3) - N/A
- [x] VQ-08: Image Size (2)

### Code Quality (XX/20)
- [x] CQ-01: KISS Structure (5)
- [x] CQ-02: Reproducibility (4)
- [x] CQ-03: Library Idioms (4)
- [x] CQ-04: Clean Imports (2)
- [x] CQ-05: Helpful Comments (2)
- [x] CQ-06: No Deprecated API (2)
- [x] CQ-07: Output Correct (1)

### Issues Found
1. **VQ-03 FAILED**: Red-green color combination is not colorblind-safe
   - Fix: Use `colors=['#306998', '#FFD43B']` from pyplots palette

### AI Feedback for Next Attempt
> Replace red-green colors with colorblind-safe palette

### Verdict: APPROVED / REJECTED
```

### 7. Take Action Based on Result

**APPROVED** (score >= 85):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-approved --add-label "quality:${SCORE}"
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-approved
```

**REJECTED** (score < 85):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-rejected --add-label "quality:${SCORE}"
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-rejected
```

## Important

- This is a **${LIBRARY}-only** review - focus only on this library
- Post feedback to **Sub-Issue #${SUB_ISSUE_NUMBER}**, NOT the main issue
- Be specific about what failed and how to fix it
- Mark criteria as N/A when not applicable (e.g., legend for single-series)
