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

### 5. Check for Auto-Reject (AR-08)

**For static libraries (matplotlib, seaborn, plotnine) only:**

Before scoring, check if the implementation fakes interactive features:
- Simulated tooltips (annotation boxes styled as hover tooltips)
- Simulated selection/hover states
- Drawn UI controls (buttons, sliders)
- Code comments mentioning "simulating hover/click/interactivity"

If found: Score = 0, verdict = REJECTED, note AR-08 violation.

### 6. Evaluate Using 6-Category Criteria

Read `prompts/quality-criteria.md` and evaluate:

#### Visual Quality (30 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| VQ-01 | Text Legibility | 8 | Font sizes explicitly set? Readable at full size? |
| VQ-02 | No Overlap | 6 | All text readable? No collisions? |
| VQ-03 | Element Visibility | 6 | Markers/lines adapted to density? |
| VQ-04 | Color Accessibility | 4 | Colorblind-safe? Good contrast? |
| VQ-05 | Layout & Canvas | 4 | Good proportions? Nothing cut off? |
| VQ-06 | Axis Labels & Title | 2 | Descriptive with units? |

#### Design Excellence (20 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| DE-01 | Aesthetic Sophistication | 8 | Professional polish? Custom palette? Intentional hierarchy? |
| DE-02 | Visual Refinement | 6 | Spines removed? Grid subtle? Whitespace generous? |
| DE-03 | Data Storytelling | 6 | Annotations? Narrative emphasis? Guides the viewer? |

**Defaults:** DE-01=4, DE-02=2, DE-03=2. Raise only with evidence.

#### Spec Compliance (15 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| SC-01 | Plot Type | 5 | Correct chart type? |
| SC-02 | Required Features | 4 | All features from spec? |
| SC-03 | Data Mapping | 3 | X/Y correct? Axes show all data? |
| SC-04 | Title & Legend | 3 | `{spec-id} · {library} · pyplots.ai`? Legend labels match? |

#### Data Quality (15 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| DQ-01 | Feature Coverage | 6 | Shows ALL aspects of plot type? |
| DQ-02 | Realistic Context | 5 | Real-world plausible AND neutral? |
| DQ-03 | Appropriate Scale | 4 | Sensible values for domain? |

#### Code Quality (10 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| CQ-01 | KISS Structure | 3 | No functions/classes? |
| CQ-02 | Reproducibility | 2 | Seed or deterministic? |
| CQ-03 | Clean Imports | 2 | Only used imports? |
| CQ-04 | Code Elegance | 2 | Appropriate complexity? No fake UI? |
| CQ-05 | Output & API | 1 | Saves as plot.png? Current API? |

#### Library Mastery (10 pts)
| ID | Criterion | Max | Check |
|----|-----------|-----|-------|
| LM-01 | Idiomatic Usage | 5 | Library's recommended patterns? High-level API? |
| LM-02 | Distinctive Features | 5 | Features unique to this library? |

**Defaults:** LM-01=3, LM-02=1. Raise only with evidence.

### 7. Apply Score Caps

| Condition | Max Score |
|-----------|-----------|
| VQ-02 = 0 (severe overlap) | 49 |
| VQ-03 = 0 (invisible elements) | 49 |
| SC-01 = 0 (wrong plot type) | 40 |
| DQ-02 = 0 (controversial data) | 49 |
| DE-01 ≤ 2 AND DE-03 ≤ 2 (generic + no storytelling) | 75 |
| CQ-04 = 0 (fake functionality) | 70 |

### 8. Post Verdict to Sub-Issue #${SUB_ISSUE_NUMBER}

Use this EXACT format:

```markdown
## AI Review - Attempt ${ATTEMPT}/3

### Score: XX/100

| Category | Score | Max |
|----------|-------|-----|
| Visual Quality | XX | 30 |
| Design Excellence | XX | 20 |
| Spec Compliance | XX | 15 |
| Data Quality | XX | 15 |
| Code Quality | XX | 10 |
| Library Mastery | XX | 10 |
| **Total** | **XX** | **100** |

### Visual Quality (XX/30)
- [x] VQ-01: Text Legibility (X/8)
- [x] VQ-02: No Overlap (X/6)
- [x] VQ-03: Element Visibility (X/6)
- [x] VQ-04: Color Accessibility (X/4)
- [x] VQ-05: Layout & Canvas (X/4)
- [x] VQ-06: Axis Labels & Title (X/2)

### Design Excellence (XX/20)
- [ ] DE-01: Aesthetic Sophistication (X/8) - Generic defaults
- [ ] DE-02: Visual Refinement (X/6) - Minimal customization
- [ ] DE-03: Data Storytelling (X/6) - No annotations or narrative

### Spec Compliance (XX/15)
- [x] SC-01: Plot Type (X/5)
- [x] SC-02: Required Features (X/4)
- [x] SC-03: Data Mapping (X/3)
- [x] SC-04: Title & Legend (X/3)

### Data Quality (XX/15)
- [x] DQ-01: Feature Coverage (X/6)
- [x] DQ-02: Realistic Context (X/5)
- [x] DQ-03: Appropriate Scale (X/4)

### Code Quality (XX/10)
- [x] CQ-01: KISS Structure (X/3)
- [x] CQ-02: Reproducibility (X/2)
- [x] CQ-03: Clean Imports (X/2)
- [x] CQ-04: Code Elegance (X/2)
- [x] CQ-05: Output & API (X/1)

### Library Mastery (XX/10)
- [x] LM-01: Idiomatic Usage (X/5)
- [ ] LM-02: Distinctive Features (X/5) - Generic usage

### Score Caps Applied
- [ ] None / [describe cap if applied]

### Issues Found
1. **DE-01 LOW**: Generic styling with default colors and no design thought
   - Fix: Custom palette, remove top/right spines, refine typography
2. **DE-03 LOW**: No annotations or data storytelling
   - Fix: Add annotations highlighting key data points or trends

### AI Feedback for Next Attempt
> Improve design excellence: remove top/right spines, use subtle y-axis-only grid, add annotations to highlight key patterns. Consider a more refined color palette.

### Verdict: APPROVED / REJECTED
```

### 9. Take Action Based on Result

**APPROVED** (score >= 90):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-approved --add-label "quality:${SCORE}"
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-approved
```

**REJECTED** (score < 90):
```bash
gh pr edit ${PR_NUMBER} --add-label ai-rejected --add-label "quality:${SCORE}"
gh issue edit ${SUB_ISSUE_NUMBER} --remove-label reviewing --add-label ai-rejected
```

## Important

- This is a **${LIBRARY}-only** review - focus only on this library
- Post feedback to **Sub-Issue #${SUB_ISSUE_NUMBER}**, NOT the main issue
- Be specific about what failed and how to fix it
- Mark criteria as N/A when not applicable (e.g., legend for single-series)
- **Score strictly**: median implementation should score 72-78, not 90+
- **Design Excellence defaults are low**: DE-01=4, DE-02=2, DE-03=2 — raise only with evidence
