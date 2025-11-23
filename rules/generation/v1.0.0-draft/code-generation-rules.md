# Code Generation Rules v1.0.0-draft

## Metadata
- **Version**: v1.0.0-draft
- **Type**: Generation
- **Status**: draft
- **Last Updated**: 2025-01-23
- **Author**: Claude (extracted from docs)

## Purpose

Define how to generate plot implementation code from Markdown specifications.

**Source**: Extracted from `docs/workflow.md`, `docs/development.md`, and `docs/architecture/specs-guide.md`

---

## Input

### Required
1. **Spec Markdown**: Complete spec file from `specs/{spec-id}.md`
2. **Target Library**: matplotlib, seaborn, plotly, bokeh, or altair
3. **Variant**: default, {style}_style, or py{version}

### Optional
- Python version target (default: 3.10+)
- Style constraints
- Custom quality criteria

---

## Output Requirements

### File Structure

```python
"""
{spec-id}: {Title}
Implementation for: {library}
Variant: {variant}
Python: {python_version}+
"""

import {plotting_library} as plt  # or seaborn as sns, etc.
import pandas as pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure  # or appropriate type


def create_plot(
    data: pd.DataFrame,
    {required_params}: {types},
    {optional_params}: {types} = {defaults},
    **kwargs
) -> Figure:  # or appropriate return type
    """
    {Description from spec}

    Args:
        data: Input DataFrame with required columns
        {param}: {description from spec}
        **kwargs: Additional parameters passed to plotting function

    Returns:
        {Library} Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({...})
        >>> fig = create_plot(data, ...)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [{required_columns}]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Create figure
    {figure_creation}

    # Plot data
    {plotting_code}

    # Apply styling
    {styling_code}

    # Labels and title
    {label_code}

    # Layout
    plt.tight_layout()  # or equivalent

    return fig


if __name__ == '__main__':
    # Sample data for testing
    {sample_data}

    # Create plot
    fig = create_plot(data, ...)

    # Save for inspection
    plt.savefig('test_output.png', dpi=150)
    print("Plot saved to test_output.png")
```

---

## Generation Process

### Step 1: Analyze Spec

From `docs/architecture/specs-guide.md`:

1. **Parse Spec Sections**:
   - Title → Function docstring
   - Description → Extended documentation
   - Data Requirements → Required parameters
   - Optional Parameters → Optional parameters with defaults
   - Quality Criteria → Checklist for self-review
   - Expected Output → Understanding of what to create

2. **Extract Parameters**:
   ```markdown
   ## Data Requirements
   - **x**: Numeric values for x-axis

   ## Optional Parameters
   - `color`: Point color (default: "blue")
   ```

   Becomes:
   ```python
   def create_plot(
       data: pd.DataFrame,
       x: str,  # Required
       color: str = "blue",  # Optional
       **kwargs
   ) -> Figure:
   ```

### Step 2: Library Selection

From `docs/workflow.md` (lines 119-127):

**Rules**:
- **matplotlib**: Always implement (universal support)
- **seaborn**: Auto-select for: heatmap, violin, box, pair plots, distributions
- **plotly**: Auto-select for: interactive needs, 3D plots, animations
- **bokeh/altair**: Future support

**Selection Logic**:
```
if spec mentions "interactive" → plotly
else if plot_type in ["heatmap", "violin", "box", "pair"] → seaborn + matplotlib
else → matplotlib (default)
```

### Step 3: Code Structure

From `docs/development.md` (lines 315-421):

**Required Elements**:
1. **Module Docstring** with spec ID and library
2. **Imports** organized by category
3. **Type Hints** on all parameters
4. **Docstring** (Google style)
5. **Input Validation** before plotting
6. **Clear Error Messages** with context
7. **Plotting Logic** that follows spec
8. **Return Statement** with appropriate type

### Step 4: Quality Standards

From `docs/development.md` (lines 182-241):

**Code Quality**:
- ✅ Type hints: `def create_plot(data: pd.DataFrame, x: str) -> Figure:`
- ✅ Docstrings: Google style with Args, Returns, Raises, Example
- ✅ Validation: Check for empty data, missing columns
- ✅ Error messages: `f"Column '{x}' not found in {list(data.columns)}"`
- ✅ Max line length: 120 characters
- ✅ Imports: Organized (standard, third-party, local)

**Visual Quality**:
- ✅ Figure size: `figsize=(10, 6)` by default
- ✅ Axis labels: From column names or custom
- ✅ Grid: `ax.grid(True, alpha=0.3)` (subtle)
- ✅ Font sizes: Readable (≥10pt)
- ✅ Legend: If multiple series or color mapping
- ✅ Tight layout: `plt.tight_layout()` to avoid clipping

---

## Library-Specific Guidelines

### matplotlib

From `docs/development.md` (lines 332-343):

```python
# Create figure explicitly
fig, ax = plt.subplots(figsize=(10, 6))

# Use axes methods (not pyplot)
ax.scatter(...)  # ✅
plt.scatter(...) # ❌

# Styling
ax.set_xlabel(x)
ax.set_ylabel(y)
ax.grid(True, alpha=0.3)

# Layout and return
plt.tight_layout()
return fig
```

### seaborn

```python
# Use seaborn's high-level API
import seaborn as sns

# Plot with seaborn
sns.scatterplot(data=data, x=x, y=y, ax=ax)

# Get figure
fig = plt.gcf()

# Or for figure-level functions
fig = sns.relplot(data=data, x=x, y=y)

return fig
```

### plotly

```python
import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=data[x], y=data[y]))

# Styling
fig.update_layout(
    title=title,
    xaxis_title=x,
    yaxis_title=y,
    template="plotly_white"  # Clean template
)

return fig
```

---

## Self-Optimization Loop

From `docs/workflow.md` (lines 119-150):

**Process** (max 3 attempts):

1. **Generate Initial Code**:
   - Follow generation rules above
   - Implement all spec requirements
   - Apply quality standards

2. **Self-Review**:
   - Execute code to render plot
   - Check against quality criteria
   - Score 0-100

3. **Optimize if Needed** (score < 85):
   - Identify specific issues from review
   - Generate targeted fixes
   - Re-generate code
   - Repeat step 2

4. **Final Decision**:
   - If score ≥ 85: SUCCESS
   - If attempts = 3 and score < 85: FAIL

---

## Examples

### Example 1: scatter-basic-001 (matplotlib)

**Input Spec** (abbreviated):
```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Data Requirements
- **x**: Numeric values for x-axis
- **y**: Numeric values for y-axis

## Optional Parameters
- `color`: Point color or column name (default: "blue")
- `size`: Point size (default: 50)
- `alpha`: Transparency (default: 0.8)
```

**Generated Code**: (See full example in `docs/development.md:322-421`)

Key features:
- Input validation with clear errors
- Support for both direct color and column mapping
- Configurable parameters with sensible defaults
- Complete docstring
- Standalone test block

---

## Common Patterns

### Pattern: Optional Column Mapping

Many plots support both direct values and column mapping:

```python
def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,  # Can be color name OR column name
    ...
) -> Figure:
    """..."""

    # Determine if color is a column or a direct value
    if color and color in data.columns:
        # Color mapping
        scatter = ax.scatter(data[x], data[y], c=data[color], ...)
        plt.colorbar(scatter, label=color)
    else:
        # Direct color
        ax.scatter(data[x], data[y], color=color or 'blue', ...)
```

### Pattern: Validation with Context

```python
# ✅ Good: Helpful error message
if x not in data.columns:
    available = ", ".join(data.columns)
    raise KeyError(f"Column '{x}' not found. Available columns: {available}")

# ❌ Bad: Unclear error
if x not in data.columns:
    raise KeyError("Column not found")
```

### Pattern: Flexible Styling

```python
def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs
) -> Figure:
    """Allow customization of labels"""

    ax.set_xlabel(xlabel or x)  # Use custom or column name
    ax.set_ylabel(ylabel or y)

    if title:
        ax.set_title(title)
```

---

## Known Issues (Draft Version)

These are areas that need refinement:

1. **Library Selection**: Currently manual, needs automated logic
2. **Self-Review**: Criteria not yet calibrated
3. **Optimization Feedback**: Loop not yet implemented
4. **Error Handling**: Edge cases not fully covered
5. **Performance**: No optimization for large datasets
6. **Accessibility**: Colorblind safety not automatically enforced

---

## Next Steps

Before promoting to v1.0.0:

1. **Test with Real Specs**: Generate 5-10 plots
2. **Refine Criteria**: Adjust based on results
3. **Implement Self-Review**: Build the feedback loop
4. **Calibrate Scoring**: Ensure thresholds make sense
5. **Document Learnings**: Update this file with findings

---

## References

- `docs/workflow.md`: Automation workflow (lines 1-678)
- `docs/architecture/specs-guide.md`: Spec template (lines 1-707)
- `docs/development.md`: Code standards (lines 1-731)
- `docs/architecture/repository-structure.md`: File organization (lines 1-407)

---

*This is a DRAFT. Treat as starting point, not final specification.*
