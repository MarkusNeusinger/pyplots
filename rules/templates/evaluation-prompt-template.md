# LLM Evaluation Prompt v{VERSION}

## Metadata
- **Version**: {VERSION}
- **Type**: Evaluation Prompt
- **Status**: {STATUS}
- **Last Updated**: {DATE}
- **Author**: {AUTHOR}
- **Target LLMs**: Claude, Gemini, GPT-4V

## Purpose

Define how LLMs should evaluate generated plot quality. This prompt is used for:
- Multi-LLM consensus evaluation
- Final approval before deployment
- A/B testing of rule versions

---

## System Prompt

```
You are an expert data visualization quality evaluator. Your task is to objectively assess whether a generated plot meets specified quality criteria.

You will be shown:
1. The original plot specification (Markdown)
2. The generated plot image (PNG)
3. Quality criteria checklist

Your evaluation should be:
- Objective and based on observable facts
- Specific about what works and what doesn't
- Constructive in suggesting improvements
- Consistent with other evaluators' assessments

Do not be lenient. Only approve plots that truly meet all criteria.
```

---

## Input Format

### 1. Spec Markdown

```markdown
# {spec-id}: {Title}

## Description
{Description}

## Data Requirements
- **{param}**: {Description}

## Optional Parameters
- `{param}`: {Description}

## Quality Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Expected Output
{Description of what plot should look like}
```

### 2. Generated Image

- Format: PNG
- Resolution: Typically 1000x600 pixels
- Shows the actual output that will be used

### 3. Implementation Details (optional)

- Library used (matplotlib, seaborn, etc.)
- Variant (default, style, etc.)
- Generation attempt number (1st, 2nd, or 3rd)

---

## Evaluation Instructions

### Step 1: Load Spec Quality Criteria

Read the quality criteria from the spec:

```markdown
## Quality Criteria
- [ ] X and Y axes are labeled with column names
- [ ] Grid is visible but subtle
- [ ] Points are clearly distinguishable
- [ ] No overlapping axis labels
- [ ] Legend is shown if color/size mapping is used
```

These are the PRIMARY criteria. The plot must meet these to pass.

### Step 2: Visual Inspection

Carefully examine the generated plot image:

**Check for**:
1. **Axes and Labels**:
   - Are X and Y axes labeled?
   - Are labels descriptive and readable?
   - Are tick labels readable?
   - Is the title present (if specified)?

2. **Data Representation**:
   - Is the data correctly visualized?
   - Are the plot type and data type compatible?
   - Is the scale appropriate?
   - Are axes not inverted accidentally?

3. **Styling**:
   - Is the grid visible but not overwhelming?
   - Are colors appropriate?
   - Are fonts readable (not too small)?
   - Is the figure size appropriate?

4. **Legend and Annotations**:
   - Is legend present if needed?
   - Is legend positioned well (not covering data)?
   - Are all elements properly labeled?

5. **Text Clarity**:
   - Is any text overlapping?
   - Are all text elements readable?
   - Are fonts appropriately sized?

6. **Accessibility**:
   - Are colors colorblind-safe (if multiple colors)?
   - Is contrast sufficient?
   - Are elements distinguishable?

### Step 3: Criterion-by-Criterion Evaluation

For each criterion in the spec's Quality Criteria section:

```
Criterion: "X and Y axes are labeled with column names"

Check:
1. Look at the image
2. Verify both axes have labels
3. Confirm labels are descriptive (not just "x", "y")

Result: MET / NOT MET

If NOT MET, explain:
- What is missing or wrong
- How to fix it
```

### Step 4: Scoring

Use this rubric:

**Score Calculation**:
- Start with 50 points (baseline)
- For each criterion MET: +5 to +10 points (based on importance)
- For each criterion NOT MET: -5 to -10 points
- Final score: Clamped to 0-100

**Thresholds**:
- **90-100**: Excellent - All criteria met, production-ready
- **85-89**: Good - Minor issues only, acceptable
- **75-84**: Needs improvement - Regeneration recommended
- **< 75**: Rejected - Major issues, must regenerate

### Step 5: Feedback Generation

Provide actionable feedback:

**Structure**:
```
Criteria Met: [✓ list of IDs]
Criteria Failed: [✗ list of IDs]

Issues Found:
1. {Specific issue with evidence from image}
2. {Another specific issue}

Suggestions for Improvement:
1. {Concrete action to fix issue 1}
2. {Concrete action to fix issue 2}

Overall Assessment:
{Brief summary of quality}
```

**Good Feedback Example**:
```
Issues Found:
1. X-axis labels are overlapping, making them unreadable
2. Grid alpha is too high (appears to be 1.0), overwhelming the data points

Suggestions:
1. Rotate x-axis labels 45 degrees: plt.xticks(rotation=45)
2. Reduce grid alpha to 0.3: ax.grid(True, alpha=0.3)
```

**Bad Feedback Example**:
```
Issues Found:
1. Plot doesn't look good
2. Something is wrong with the labels

Suggestions:
1. Make it better
```

---

## Output Format

### JSON Structure

```json
{
  "score": 0-100,
  "pass": true/false,
  "criteria_met": ["id1", "id2", "id3"],
  "criteria_failed": ["id4", "id5"],
  "issues": [
    "Specific issue 1",
    "Specific issue 2"
  ],
  "suggestions": [
    "Concrete fix for issue 1",
    "Concrete fix for issue 2"
  ],
  "confidence": 0.0-1.0,
  "notes": "Any additional observations"
}
```

### Field Descriptions

**score** (integer, 0-100):
- Objective quality score
- Based on criteria evaluation
- Use scoring rubric above

**pass** (boolean):
- True if score ≥ 85
- False otherwise

**criteria_met** (array of strings):
- IDs of criteria that passed
- Use exact criterion text from spec

**criteria_failed** (array of strings):
- IDs of criteria that failed
- Use exact criterion text from spec

**issues** (array of strings):
- Specific problems found
- Observable, not subjective
- Referenced to image evidence

**suggestions** (array of strings):
- Actionable improvements
- Concrete code changes if possible
- Prioritized (most important first)

**confidence** (float, 0.0-1.0):
- How confident you are in this evaluation
- 1.0 = Very confident
- 0.5 = Somewhat uncertain
- < 0.5 = Low confidence, might need human review

**notes** (string, optional):
- Additional context
- Ambiguous cases
- Reasons for judgment calls

---

## Example Evaluation

### Input Spec

```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Quality Criteria
- [ ] X and Y axes are labeled with column names
- [ ] Grid is visible but subtle (not overpowering the data)
- [ ] Points are clearly distinguishable (appropriate size and alpha)
- [ ] No overlapping axis labels or tick marks
- [ ] Legend is shown if color/size mapping is used
```

### Generated Image

*(Image shows scatter plot with overlapping x-axis labels and no grid)*

### Evaluation Output

```json
{
  "score": 72,
  "pass": false,
  "criteria_met": [
    "X and Y axes are labeled with column names",
    "Points are clearly distinguishable",
    "Legend is shown if color/size mapping is used"
  ],
  "criteria_failed": [
    "Grid is visible but subtle",
    "No overlapping axis labels or tick marks"
  ],
  "issues": [
    "X-axis tick labels are overlapping, making them unreadable in the 5-8 range",
    "No grid is visible, making it harder to read values",
    "Grid criterion is marked as required but not present"
  ],
  "suggestions": [
    "Add grid with low alpha: ax.grid(True, alpha=0.3)",
    "Rotate x-axis labels to prevent overlap: plt.xticks(rotation=45)",
    "Alternatively, reduce number of tick marks if rotation is not suitable"
  ],
  "confidence": 0.95,
  "notes": "Clear issues with overlapping labels and missing grid. Score would be 85+ if these two issues were fixed."
}
```

---

## Consistency Guidelines

### Be Objective

❌ **Subjective**: "The plot looks ugly"
✅ **Objective**: "Font size is 6pt, below the 10pt minimum requirement"

### Be Specific

❌ **Vague**: "Labels are bad"
✅ **Specific**: "X-axis labels overlap between positions 5-8, obscuring the text"

### Be Actionable

❌ **Not actionable**: "Fix the colors"
✅ **Actionable**: "Use a colorblind-safe palette like 'viridis' or 'tab10'"

### Be Consistent

**Same plot, same score**:
- If you see the same plot twice, score should be the same
- Don't let order bias your evaluation
- Use the criteria, not your mood

---

## Edge Cases

### Case 1: Criterion is Ambiguous

**Situation**: "Grid is visible but subtle" - what's "subtle"?

**Approach**:
1. Use common sense (alpha ≤ 0.5 is reasonable)
2. Note ambiguity in feedback
3. If truly unclear, mark confidence lower

```json
{
  "score": 85,
  "confidence": 0.75,
  "notes": "Grid alpha appears to be around 0.4-0.6, which is borderline for 'subtle'. Marking as pass but noting ambiguity."
}
```

### Case 2: Extra Features Not in Spec

**Situation**: Plot has extra features not mentioned in spec

**Approach**:
- Don't penalize for extra features (unless they hurt quality)
- Focus on whether spec requirements are met
- Can mention extras positively in notes

### Case 3: Minor vs Major Issues

**Minor** (acceptable for score 85-89):
- Slightly suboptimal styling
- Edge case not handled
- Documentation could be better

**Major** (requires score < 85):
- Criterion explicitly failed
- Data misrepresented
- Unusable in production

### Case 4: Multiple Failure Points

**Situation**: Multiple criteria failed

**Approach**:
- List all issues
- Prioritize by impact
- Cumulative penalty (score drops significantly)

```json
{
  "score": 65,
  "criteria_failed": ["grid", "labels", "colors"],
  "issues": [
    "No grid visible (required)",
    "X-axis labels overlapping (required)",
    "Colors not colorblind-safe (required)"
  ],
  "suggestions": [
    "1. Add grid: ax.grid(True, alpha=0.3)",
    "2. Rotate labels: plt.xticks(rotation=45)",
    "3. Use colorblind palette: cmap='tab10'"
  ],
  "notes": "Multiple critical issues. All three must be fixed before approval."
}
```

---

## Multi-LLM Consensus

When using multiple LLMs (Claude, Gemini, GPT):

### Individual Evaluation

Each LLM evaluates independently:
- No communication between LLMs
- Same inputs
- Same instructions
- Same output format

### Aggregation

```python
def calculate_consensus(
    evaluations: list[LLMEvaluation]
) -> ConsensusResult:
    """
    Calculate consensus from multiple LLM evaluations

    Rules:
    - Median score (robust to outliers)
    - Majority vote on pass/fail
    - Intersection of criteria_met (all agree)
    - Union of issues (any LLM found it)
    """
    scores = [e.score for e in evaluations]
    median_score = statistics.median(scores)

    pass_votes = sum(e.pass for e in evaluations)
    consensus_pass = pass_votes >= len(evaluations) / 2

    # Criteria all LLMs agree on
    criteria_met = set.intersection(*[
        set(e.criteria_met) for e in evaluations
    ])

    # Issues any LLM found
    all_issues = list(set.union(*[
        set(e.issues) for e in evaluations
    ]))

    return ConsensusResult(
        score=median_score,
        pass=consensus_pass,
        criteria_met=list(criteria_met),
        issues=all_issues,
        agreement_rate=pass_votes / len(evaluations)
    )
```

### Disagreement Handling

**If LLMs disagree significantly** (>10 points apart):
- Flag for human review
- Log evaluations for analysis
- May indicate ambiguous spec or edge case

---

## Calibration

### Initial Calibration

Before using evaluation prompts at scale:

1. **Test Set**: Evaluate 10 plots with known quality
2. **Compare Scores**: Check LLM scores vs expected scores
3. **Adjust Thresholds**: If LLMs are too lenient/strict, adjust
4. **Iterate**: Refine prompt based on results

### Continuous Monitoring

Track evaluation metrics:
- Average score over time
- Pass rate
- LLM agreement rate
- Human override rate (if humans review)

---

## Prompt Versions

### Changelog

When creating a new version:

```yaml
# In metadata.yaml
changelog:
  - "Clarified 'subtle grid' definition (alpha ≤ 0.5)"
  - "Added confidence field to output format"
  - "Improved feedback specificity guidelines"
  - "Added edge case handling section"
```

### A/B Testing Prompts

Test prompt versions just like rule versions:

```python
# Test two prompt versions
results_v1 = evaluate_with_prompt(plots, prompt_version="v1.0.0")
results_v2 = evaluate_with_prompt(plots, prompt_version="v2.0.0")

# Compare consistency, strictness, agreement
compare_prompt_versions(results_v1, results_v2)
```

---

## Related Documents

- [Generation Rules Template](./generation-rules-template.md)
- [Quality Criteria Template](./quality-criteria-template.md)
- [Rule Versioning Guide](../../docs/architecture/rule-versioning.md)
- [A/B Testing Guide](../../docs/concepts/ab-testing-rules.md)

---

*Customize this prompt for your LLM and domain*
