# Quality Criteria v{VERSION}

## Metadata
- **Version**: {VERSION}
- **Type**: Quality Criteria
- **Status**: {STATUS}
- **Last Updated**: {DATE}
- **Author**: {AUTHOR}

## Purpose

Define what constitutes a high-quality plot implementation. These criteria are used for:
1. **Self-review**: AI evaluates its own generated code
2. **Quality scoring**: Objective measurement (0-100)
3. **Feedback generation**: Specific improvement suggestions
4. **A/B testing**: Compare rule versions

---

## Scoring Scale

**Range**: 0-100

**Thresholds**:
- **90-100**: Excellent - All criteria met, production-ready
- **85-89**: Good - Minor issues only, acceptable
- **75-84**: Needs improvement - Some criteria failed
- **< 75**: Rejected - Major issues, regeneration required

**Pass Threshold**: ≥ 85

---

## Criteria Categories

### 1. Visual Quality (40% weight)

Appearance, readability, aesthetics.

### 2. Code Quality (30% weight)

Code structure, documentation, maintainability.

### 3. Correctness (20% weight)

Data accurately represented, no errors.

### 4. Accessibility (10% weight)

Colorblind-safe, readable fonts, screen reader compatibility.

---

## Criteria Definitions

### Visual Quality

#### VQ-001: Axes Labeled

- **ID**: `axes_labeled`
- **Weight**: 1.0 (critical)
- **Requirement**: Both X and Y axes must have descriptive labels
- **Check**:
  - `ax.get_xlabel()` returns non-empty string
  - `ax.get_ylabel()` returns non-empty string
  - Labels are descriptive (not just "x" or "y")
- **Failure Impact**: Major - Plot is unusable without axis labels
- **Examples**:
  - ✅ Good: xlabel="Age (years)", ylabel="Income ($)"
  - ❌ Bad: xlabel="x", ylabel="" (empty)
  - ❌ Bad: No labels at all

**Scoring**:
- Met: +10 points
- Not met: -10 points

---

#### VQ-002: Grid Visibility

- **ID**: `grid_visible`
- **Weight**: 0.5 (nice-to-have)
- **Requirement**: Grid should be visible but subtle (alpha ≤ 0.5)
- **Check**:
  - Grid is enabled
  - Grid alpha ≤ 0.5
  - Grid doesn't overpower data
- **Failure Impact**: Minor - Aesthetic issue only
- **Examples**:
  - ✅ Good: `ax.grid(True, alpha=0.3)`
  - ⚠️ Acceptable: No grid (if plot is simple)
  - ❌ Bad: Grid too prominent (alpha=1.0)

**Scoring**:
- Met: +5 points
- Not met: -2 points
- Absent (simple plot): 0 points (neutral)

---

#### VQ-003: No Overlapping Text

- **ID**: `no_overlapping_text`
- **Weight**: 0.9 (important)
- **Requirement**: All text elements must be readable (no overlap)
- **Check**:
  - Axis labels don't overlap
  - Tick labels don't overlap
  - Legend doesn't cover data
  - Title doesn't overlap with plot
- **Failure Impact**: Medium - Reduces readability
- **Examples**:
  - ✅ Good: `plt.xticks(rotation=45)` for long labels
  - ❌ Bad: Overlapping x-axis labels
  - ❌ Bad: Legend covering data points

**Scoring**:
- Met: +9 points
- Partial overlap: -5 points
- Severe overlap: -9 points

---

#### VQ-004: Appropriate Figure Size

- **ID**: `figure_size_appropriate`
- **Weight**: 0.6
- **Requirement**: Figure size is appropriate for data and use case
- **Check**:
  - Not too small (< 6 inches)
  - Not too large (> 20 inches)
  - Aspect ratio makes sense
  - Default: (10, 6) inches is a good balance
- **Failure Impact**: Medium - Affects usability
- **Examples**:
  - ✅ Good: `figsize=(10, 6)`
  - ⚠️ Acceptable: `figsize=(8, 5)` or `figsize=(12, 8)`
  - ❌ Bad: `figsize=(3, 3)` (too small)

**Scoring**:
- Met: +6 points
- Slightly off: -2 points
- Way off: -6 points

---

#### VQ-005: Legend Present (if needed)

- **ID**: `legend_present`
- **Weight**: 0.8
- **Requirement**: Legend shown if plot has multiple series or color mapping
- **Check**:
  - If multiple series: legend must be present
  - If color mapping: colorbar or legend required
  - If single series: legend optional
  - Legend is positioned well (not covering data)
- **Failure Impact**: Medium - Can't distinguish series without legend
- **Examples**:
  - ✅ Good: `ax.legend()` for multi-series
  - ✅ Good: `plt.colorbar(scatter, label='Value')`
  - ❌ Bad: Multiple series without legend

**Scoring**:
- Met: +8 points
- Not met (but needed): -8 points
- N/A (single series): 0 points

---

### Code Quality

#### CQ-001: Type Hints Present

- **ID**: `type_hints_present`
- **Weight**: 0.7
- **Requirement**: All parameters and return type must have type hints
- **Check**:
  - Function signature has type hints
  - All parameters annotated
  - Return type specified
  - Uses modern syntax (`|` for union on 3.10+)
- **Failure Impact**: Medium - Reduces code maintainability
- **Examples**:
  - ✅ Good: `def create_plot(data: pd.DataFrame, x: str) -> Figure:`
  - ❌ Bad: `def create_plot(data, x):`

**Scoring**:
- Met: +7 points
- Partial: -3 points
- Missing: -7 points

---

#### CQ-002: Complete Docstring

- **ID**: `docstring_complete`
- **Weight**: 0.8
- **Requirement**: Function has complete docstring (Google style)
- **Check**:
  - One-line summary present
  - Args section with all parameters
  - Returns section
  - Raises section (if applicable)
  - Example section (at least one)
- **Failure Impact**: Medium - Documentation is important
- **Examples**:
  - ✅ Good: Complete Google-style docstring
  - ❌ Bad: `"""Create plot"""` (too brief)

**Scoring**:
- Complete: +8 points
- Partial: -4 points
- Missing/incomplete: -8 points

---

#### CQ-003: Input Validation

- **ID**: `input_validation`
- **Weight**: 1.0
- **Requirement**: Input parameters must be validated
- **Check**:
  - Check data not empty
  - Check required columns exist
  - Check parameter ranges if applicable
  - Clear error messages
- **Failure Impact**: Major - No validation = crashes
- **Examples**:
  - ✅ Good: Comprehensive validation with clear errors
  - ❌ Bad: No validation (will crash on bad input)

**Scoring**:
- Met: +10 points
- Partial: +5 points
- Missing: -10 points

---

#### CQ-004: Error Messages Clear

- **ID**: `error_messages_clear`
- **Weight**: 0.6
- **Requirement**: Error messages must be informative
- **Check**:
  - Explain what went wrong
  - Suggest how to fix
  - Include relevant context
- **Failure Impact**: Minor - Affects debugging experience
- **Examples**:
  - ✅ Good: `f"Column '{x}' not found in {list(data.columns)}"`
  - ❌ Bad: `"Error"` or `"Not found"`

**Scoring**:
- Met: +6 points
- Vague: -3 points
- Very poor: -6 points

---

#### CQ-005: No Hardcoded Values

- **ID**: `no_hardcoded_values`
- **Weight**: 0.5
- **Requirement**: Values should be parameterized, not hardcoded
- **Check**:
  - Magic numbers are parameters or constants
  - Colors, sizes, etc. are configurable
  - Exceptions: Mathematical constants (pi, e, etc.)
- **Failure Impact**: Minor - Reduces reusability
- **Examples**:
  - ✅ Good: `size: float = 50` (parameter)
  - ❌ Bad: `ax.scatter(..., s=50)` (hardcoded)

**Scoring**:
- Met: +5 points
- Some hardcoded: -2 points
- Many hardcoded: -5 points

---

### Correctness

#### CR-001: Data Accurately Represented

- **ID**: `data_accurate`
- **Weight**: 1.0 (critical)
- **Requirement**: Plot must accurately represent the data
- **Check**:
  - Correct columns plotted
  - Scales are appropriate
  - No data manipulation errors
  - Axes not inverted accidentally
- **Failure Impact**: Critical - Wrong plot is worse than no plot
- **Examples**:
  - ✅ Good: Plot shows what spec requires
  - ❌ Bad: Plotting wrong columns
  - ❌ Bad: Data transformed incorrectly

**Scoring**:
- Met: +10 points
- Minor inaccuracy: -5 points
- Major inaccuracy: -10 points

---

#### CR-002: Handles Edge Cases

- **ID**: `edge_cases_handled`
- **Weight**: 0.7
- **Requirement**: Code gracefully handles edge cases
- **Check**:
  - Empty data
  - Missing columns
  - NaN/null values
  - Single data point
  - Very large datasets
- **Failure Impact**: Medium - May crash in production
- **Examples**:
  - ✅ Good: Validates and gives clear error
  - ❌ Bad: Crashes with cryptic error

**Scoring**:
- Met: +7 points
- Partial: +3 points
- Poor: -7 points

---

#### CR-003: Follows Spec Requirements

- **ID**: `spec_compliance`
- **Weight**: 1.0 (critical)
- **Requirement**: Implements all spec requirements
- **Check**:
  - All required parameters present
  - All optional parameters supported
  - Behavior matches spec description
  - Quality criteria from spec met
- **Failure Impact**: Critical - Not following spec
- **Examples**:
  - ✅ Good: All spec requirements implemented
  - ❌ Bad: Missing optional parameters
  - ❌ Bad: Different behavior than described

**Scoring**:
- All met: +10 points
- Most met: +5 points
- Many missing: -10 points

---

### Accessibility

#### AC-001: Colorblind-Safe Palette

- **ID**: `colorblind_safe`
- **Weight**: 0.8
- **Requirement**: When using colors, use colorblind-safe palette
- **Check**:
  - Uses colorblind-safe palettes (tab10, viridis, etc.)
  - Avoids red-green combinations
  - If custom colors, they're distinguishable
- **Failure Impact**: Medium - Excludes colorblind users
- **Examples**:
  - ✅ Good: `cmap='viridis'` or `cmap='tab10'`
  - ❌ Bad: Red-green palette
  - ⚠️ Acceptable: Single color (no mapping)

**Scoring**:
- Met: +8 points
- N/A (no color mapping): 0 points
- Not met: -8 points

---

#### AC-002: Readable Font Sizes

- **ID**: `font_size_readable`
- **Weight**: 0.7
- **Requirement**: All text must be readable (minimum 10pt)
- **Check**:
  - Axis labels ≥ 10pt
  - Tick labels ≥ 9pt
  - Title ≥ 12pt
  - Legend ≥ 9pt
- **Failure Impact**: Medium - Small text is unreadable
- **Examples**:
  - ✅ Good: Default matplotlib sizes (usually OK)
  - ❌ Bad: `fontsize=6` (too small)

**Scoring**:
- Met: +7 points
- Slightly small: -3 points
- Very small: -7 points

---

## Scoring Algorithm

### Simple Sum

```python
def calculate_score(criteria_results: dict[str, bool]) -> int:
    """
    Calculate total quality score from criteria results

    Args:
        criteria_results: {criterion_id: met (True/False/None)}

    Returns:
        Score 0-100
    """
    score = 50  # Start at middle

    for criterion_id, met in criteria_results.items():
        criterion = get_criterion(criterion_id)

        if met is True:
            score += criterion.met_points
        elif met is False:
            score -= criterion.not_met_points
        # None = N/A, no change

    # Clamp to 0-100
    return max(0, min(100, score))
```

### Weighted Average (Alternative)

```python
def calculate_weighted_score(criteria_results: dict) -> int:
    """
    Weighted average based on category weights:
    - Visual Quality: 40%
    - Code Quality: 30%
    - Correctness: 20%
    - Accessibility: 10%
    """
    category_scores = {}

    for category in ['visual', 'code', 'correctness', 'accessibility']:
        criteria = get_criteria_for_category(category)
        category_score = sum(
            criterion.weight * (1.0 if criteria_results[c.id] else 0.0)
            for c in criteria
        ) / sum(c.weight for c in criteria)

        category_scores[category] = category_score * 100

    # Weighted sum
    total = (
        category_scores['visual'] * 0.40 +
        category_scores['code'] * 0.30 +
        category_scores['correctness'] * 0.20 +
        category_scores['accessibility'] * 0.10
    )

    return round(total)
```

---

## Usage Examples

### Example 1: Self-Review

```python
def self_review(code: str, spec: str) -> ReviewResult:
    """
    Evaluate generated code against quality criteria

    Process:
    1. Load quality criteria
    2. Execute code to generate plot
    3. Check each criterion
    4. Calculate score
    5. Generate feedback
    """
    criteria = load_quality_criteria(version="v1.0.0")

    # Execute and capture plot
    fig = execute_code(code)

    # Check criteria
    results = {}
    for criterion in criteria:
        results[criterion.id] = check_criterion(criterion, fig, code)

    # Calculate score
    score = calculate_score(results)

    # Generate feedback
    feedback = generate_feedback(results, criteria)

    return ReviewResult(
        score=score,
        criteria_met=[id for id, met in results.items() if met],
        criteria_failed=[id for id, met in results.items() if not met],
        feedback=feedback
    )
```

### Example 2: Compare Implementations

```python
def compare_implementations(spec_id: str, libraries: list[str]) -> Comparison:
    """
    Compare quality across different library implementations
    """
    results = {}

    for library in libraries:
        code = load_implementation(spec_id, library, "default")
        review = self_review(code, load_spec(spec_id))
        results[library] = review

    # Find best
    best_library = max(results, key=lambda lib: results[lib].score)

    return Comparison(
        results=results,
        best=best_library,
        best_score=results[best_library].score
    )
```

---

## Customization

### Project-Specific Criteria

Add criteria specific to your organization:

```markdown
#### PS-001: Brand Colors Used

- **ID**: `brand_colors_used`
- **Weight**: 0.5
- **Requirement**: Use company brand colors when applicable
- **Check**: Colors match brand guidelines
- **Examples**:
  - ✅ Good: `colors=['#FF6B6B', '#4ECDC4']` (brand colors)
  - ❌ Bad: Random colors
```

### Domain-Specific Criteria

For scientific, financial, or other domains:

```markdown
#### SCI-001: Error Bars Present

- **ID**: `error_bars_present`
- **Weight**: 0.9
- **Requirement**: Show error bars for experimental data
- **Check**: Error bars visible when uncertainty present
```

---

## Changelog Template

When creating a new version, document what changed:

```yaml
# In metadata.yaml
changelog:
  - "Added criterion AC-003: Screen reader compatibility"
  - "Increased weight of CR-001 from 0.9 to 1.0"
  - "Clarified VQ-003 definition (overlapping text)"
  - "Removed deprecated criterion VQ-006"
```

---

## Related Documents

- [Generation Rules Template](./generation-rules-template.md)
- [Evaluation Prompt Template](./evaluation-prompt-template.md)
- [Rule Versioning Guide](../../docs/architecture/rule-versioning.md)

---

*Customize this template for your specific needs*
