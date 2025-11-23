# Quality Criteria v1.0.0-draft

## Metadata
- **Version**: v1.0.0-draft
- **Type**: Quality Criteria
- **Status**: draft
- **Last Updated**: 2025-01-23
- **Extracted From**: `docs/architecture/specs-guide.md` (lines 237-279)

## Purpose

Define what constitutes a high-quality plot implementation.

**Source**: Criteria based on example quality checklists in spec documentation.

---

## Scoring

**Range**: 0-100

**Thresholds**:
- **≥ 90**: Excellent (all criteria met)
- **≥ 85**: Good (minor issues, acceptable) ← **PASS THRESHOLD**
- **75-84**: Needs improvement
- **< 75**: Rejected

---

## Visual Quality Criteria

From `docs/architecture/specs-guide.md` (example quality criteria):

### VQ-001: Axes Labeled
- **ID**: `axes_labeled`
- **Weight**: Critical (10 points)
- **Requirement**: X and Y axes must have descriptive labels
- **Check**: Both axes have non-empty, meaningful labels
- **Example**: ✅ "Age (years)" / ❌ "" (empty) or "x"

### VQ-002: Grid Visible but Subtle
- **ID**: `grid_subtle`
- **Weight**: Medium (5 points)
- **Requirement**: Grid should be present but not overpowering
- **Check**: Grid alpha ≤ 0.5
- **Example**: ✅ `ax.grid(True, alpha=0.3)` / ❌ Too prominent

### VQ-003: Points/Elements Distinguishable
- **ID**: `elements_clear`
- **Weight**: High (8 points)
- **Requirement**: Data elements must be clearly visible
- **Check**: Appropriate size, alpha, and contrast
- **Example**: ✅ size=50, alpha=0.8 / ❌ Too small or transparent

### VQ-004: No Overlapping Labels
- **ID**: `no_overlap`
- **Weight**: High (9 points)
- **Requirement**: All text elements must be readable
- **Check**: No overlapping axis labels, ticks, or legend
- **Example**: ✅ Rotated labels / ❌ Overlapping text

### VQ-005: Legend (if needed)
- **ID**: `legend_present`
- **Weight**: Medium (7 points)
- **Requirement**: Legend shown for multi-series or color mapping
- **Check**: Legend present if >1 series or color mapping used
- **Example**: ✅ `ax.legend()` when needed / ❌ Missing legend

### VQ-006: Colorblind-Safe (if applicable)
- **ID**: `colorblind_safe`
- **Weight**: Medium (6 points)
- **Requirement**: Use colorblind-safe palettes for color mapping
- **Check**: Avoid red-green, use viridis/tab10/colorblind palettes
- **Example**: ✅ `cmap='viridis'` / ❌ Red-green palette

### VQ-007: Appropriate Figure Size
- **ID**: `figure_size_ok`
- **Weight**: Low (4 points)
- **Requirement**: Figure size is reasonable (default 10x6 inches)
- **Check**: Not too small (<6") or too large (>20")
- **Example**: ✅ `figsize=(10, 6)` / ❌ `figsize=(3, 3)`

### VQ-008: Title (if provided)
- **ID**: `title_centered`
- **Weight**: Low (3 points)
- **Requirement**: Title should be centered and clear if provided
- **Check**: Title present and properly formatted when specified
- **Example**: ✅ `ax.set_title(title)` / ❌ Missing when required

---

## Code Quality Criteria

From `docs/development.md` (code standards):

### CQ-001: Type Hints Present
- **ID**: `type_hints`
- **Weight**: Medium (7 points)
- **Requirement**: All parameters and return type have type hints
- **Example**: ✅ `def create_plot(data: pd.DataFrame) -> Figure:` / ❌ No types

### CQ-002: Complete Docstring
- **ID**: `docstring_complete`
- **Weight**: High (8 points)
- **Requirement**: Google-style docstring with Args, Returns, Raises, Example
- **Example**: ✅ Complete docstring / ❌ Missing sections

### CQ-003: Input Validation
- **ID**: `validation_present`
- **Weight**: Critical (10 points)
- **Requirement**: Check for empty data and missing columns
- **Example**: ✅ Validates before plotting / ❌ No validation

### CQ-004: Clear Error Messages
- **ID**: `error_messages_clear`
- **Weight**: Medium (6 points)
- **Requirement**: Errors include context (what went wrong, what's available)
- **Example**: ✅ `f"Column '{x}' not found in {cols}"` / ❌ "Error"

### CQ-005: No Hardcoded Values
- **ID**: `no_hardcoded`
- **Weight**: Low (4 points)
- **Requirement**: Magic numbers should be parameters
- **Example**: ✅ `size: float = 50` / ❌ Hardcoded `s=50`

---

## Correctness Criteria

### CR-001: Data Accurately Represented
- **ID**: `data_accurate`
- **Weight**: Critical (10 points)
- **Requirement**: Plot shows correct data from correct columns
- **Example**: ✅ Plotting specified columns / ❌ Wrong columns

### CR-002: Spec Requirements Met
- **ID**: `spec_compliance`
- **Weight**: Critical (10 points)
- **Requirement**: All required parameters implemented
- **Example**: ✅ All spec params / ❌ Missing requirements

### CR-003: Edge Cases Handled
- **ID**: `edge_cases`
- **Weight**: Medium (5 points)
- **Requirement**: Graceful handling of empty data, NaNs, etc.
- **Example**: ✅ Raises ValueError for empty data / ❌ Crashes

---

## Scoring Formula

**Start**: 50 points (baseline)

**Add/Subtract**:
- Each criterion MET: +{weight} points
- Each criterion NOT MET: -{weight} points
- N/A criteria: 0 points (neutral)

**Clamp**: Final score between 0-100

**Example**:
```
Base: 50
+ axes_labeled (10) = 60
+ grid_subtle (5) = 65
+ elements_clear (8) = 73
+ no_overlap (9) = 82
+ legend_present (7) = 89
- colorblind_safe (-6) [failed] = 83
+ figure_size_ok (4) = 87

Total: 87 → PASS (≥85)
```

---

## Criterion Categories

By importance:

**Critical** (must have):
- axes_labeled
- validation_present
- data_accurate
- spec_compliance

**High** (important):
- no_overlap
- elements_clear
- docstring_complete

**Medium** (good to have):
- grid_subtle
- legend_present
- colorblind_safe
- type_hints
- error_messages_clear

**Low** (nice to have):
- figure_size_ok
- title_centered
- no_hardcoded

---

## Usage

### Self-Review

```python
def self_review(code: str, spec: str) -> dict:
    """Check generated code against criteria"""

    # Execute code
    fig = execute_code(code)

    # Check each criterion
    results = {}
    results['axes_labeled'] = check_axes_labeled(fig)
    results['grid_subtle'] = check_grid(fig)
    results['type_hints'] = check_type_hints(code)
    # ... etc

    # Calculate score
    score = calculate_score(results)

    return {
        'score': score,
        'criteria_met': [k for k, v in results.items() if v],
        'criteria_failed': [k for k, v in results.items() if not v]
    }
```

---

## Known Issues (Draft Version)

1. **Weights Not Calibrated**: Based on estimates, not real data
2. **Some Criteria Subjective**: "Subtle" grid needs clearer definition
3. **Missing Criteria**: No performance, accessibility details
4. **Scoring Needs Testing**: Thresholds may need adjustment

---

## Next Steps

1. Test scoring with real plots
2. Calibrate weights based on importance
3. Add more specific checks (font sizes, etc.)
4. Refine subjective criteria
5. Add performance criteria if needed

---

*DRAFT - Subject to change based on testing*
