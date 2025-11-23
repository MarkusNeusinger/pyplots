# Self-Review Checklist v1.0.0-draft

## Metadata
- **Version**: v1.0.0-draft
- **Type**: Self-Review Process
- **Status**: draft
- **Last Updated**: 2025-01-23
- **Source**: Based on `docs/workflow.md` self-optimization loop

## Purpose

Guide AI in reviewing its own generated code before considering it complete.

---

## Self-Review Process

From `docs/workflow.md` (lines 119-150):

### Step 1: Execute Code

```python
# Run the generated code with sample data
try:
    fig = execute_generated_code(code)
    execution_success = True
except Exception as e:
    execution_success = False
    error_message = str(e)
```

**Check**: Does code execute without errors?
- ✅ YES: Continue to visual inspection
- ❌ NO: Identify error, regenerate

### Step 2: Visual Inspection

Render the plot and examine the output:

**Questions to Ask**:
1. Are both axes labeled? (Check `ax.get_xlabel()`, `ax.get_ylabel()`)
2. Is the grid visible but subtle?
3. Are data points/bars/lines clearly visible?
4. Is any text overlapping?
5. Is a legend present if needed?
6. Are colors colorblind-safe if using multiple colors?
7. Is the overall appearance professional?

### Step 3: Code Review

Review the code itself:

**Checklist**:
- [ ] Type hints present on all parameters
- [ ] Docstring is complete (Args, Returns, Raises, Example)
- [ ] Input validation included (empty data, missing columns)
- [ ] Error messages are informative
- [ ] No hardcoded magic numbers
- [ ] Imports are organized
- [ ] Code is formatted (line length <120)

### Step 4: Spec Compliance

Compare against original spec:

- [ ] All required parameters implemented
- [ ] All optional parameters supported (with defaults)
- [ ] Behavior matches spec description
- [ ] Quality criteria from spec are met

---

## Scoring Guide

Assign score based on findings:

**90-100**: Perfect
- No issues found
- All criteria met
- Code executes flawlessly
- Visual quality excellent

**85-89**: Minor issues
- 1-2 small problems
- Easily fixable
- Still acceptable quality

**75-84**: Needs work
- Several criteria failed
- Visual issues present
- Should regenerate with fixes

**< 75**: Significant problems
- Major issues
- Does not meet spec
- Must regenerate

---

## Decision Logic

```
IF score >= 85:
    RETURN SUCCESS (code is good enough)

ELSE IF attempts < 3:
    GENERATE feedback for improvement
    REGENERATE code with feedback
    REPEAT self-review

ELSE:  # attempts == 3 and score < 85
    RETURN FAILURE (unable to meet criteria after 3 tries)
```

---

## Feedback Generation

When score < 85, provide specific, actionable feedback:

### Good Feedback Format

```markdown
## Issues Found

1. **X-axis labels overlapping** (VQ-004)
   - Observation: Labels between positions 5-10 are unreadable
   - Severity: High
   - Fix: Rotate labels 45 degrees: `plt.xticks(rotation=45)`

2. **Grid too prominent** (VQ-002)
   - Observation: Grid alpha appears to be 1.0
   - Severity: Medium
   - Fix: Reduce alpha: `ax.grid(True, alpha=0.3)`

3. **Missing input validation** (CQ-003)
   - Observation: No check for empty data
   - Severity: Critical
   - Fix: Add at start: `if data.empty: raise ValueError(...)`

## Optimization Strategy

1. First, fix critical issues (validation)
2. Then, fix high-severity issues (overlapping labels)
3. Finally, address medium issues (grid alpha)

## Expected Improvement

If all fixes applied, estimated new score: ~88 (PASS)
```

### Bad Feedback (Avoid)

```markdown
## Issues
- Plot doesn't look good
- Labels are bad
- Code needs improvement

## Fix
- Make it better
```

---

## Example Self-Review Session

### Attempt 1

```python
# Generated code (first try)
def create_plot(data, x, y):  # ❌ No type hints
    fig, ax = plt.subplots()
    ax.scatter(data[x], data[y], s=50)  # ❌ Hardcoded, no validation
    return fig
```

**Self-Review Result**:
- Score: 65
- Issues: No type hints, no validation, no labels, hardcoded size
- Decision: REGENERATE (< 85)

### Attempt 2

```python
# Generated code (second try, with feedback)
def create_plot(data: pd.DataFrame, x: str, y: str, size: float = 50) -> Figure:
    """Create scatter plot"""  # ❌ Docstring incomplete
    if data.empty:
        raise ValueError("Data cannot be empty")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[x], data[y], s=size)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.grid(True, alpha=1.0)  # ❌ Grid too prominent
    return fig
```

**Self-Review Result**:
- Score: 82
- Issues: Incomplete docstring, grid too prominent
- Decision: REGENERATE (< 85, fixable)

### Attempt 3

```python
# Generated code (third try, refined)
def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    size: float = 50,
    alpha: float = 0.8
) -> Figure:
    """
    Create a scatter plot

    Args:
        data: Input DataFrame
        x: Column for x-axis
        y: Column for y-axis
        size: Point size (default: 50)
        alpha: Transparency (default: 0.8)

    Returns:
        Matplotlib Figure

    Raises:
        ValueError: If data is empty
        KeyError: If columns not found
    """
    # Validation
    if data.empty:
        raise ValueError("Data cannot be empty")
    if x not in data.columns or y not in data.columns:
        raise KeyError(f"Columns not found")

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[x], data[y], s=size, alpha=alpha)

    # Styling
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
```

**Self-Review Result**:
- Score: 91
- Issues: None (all criteria met)
- Decision: SUCCESS (≥ 85)

---

## Tips for Better Self-Review

### Be Objective

❌ Subjective: "Plot looks nice"
✅ Objective: "All criteria met: axes labeled ✓, grid subtle ✓, no overlap ✓"

### Be Specific

❌ Vague: "Something wrong with labels"
✅ Specific: "X-axis labels overlap at positions 5-8"

### Be Actionable

❌ Not actionable: "Improve the code"
✅ Actionable: "Add type hints: `data: pd.DataFrame`"

### Reference Criteria

Always reference specific criterion IDs:
- "VQ-004 (no_overlap) failed: labels overlapping"
- "CQ-003 (validation_present) met: validation included"

---

## Known Limitations (Draft)

1. **Self-review not yet implemented** - This is guidance only
2. **Scoring is estimated** - Needs calibration with real data
3. **Visual inspection** - How to programmatically check?
4. **Feedback loop** - Not yet automated

---

## Next Steps

1. Implement self-review execution
2. Test with real code generation
3. Calibrate scoring thresholds
4. Automate feedback generation
5. Integrate with generation loop

---

*DRAFT - Process not yet implemented*
