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
2. **Target Library**: matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, or highcharts
3. **Variant**: default, {style}_style, or py{version}

### Optional
- Python version target (default: 3.10+)
- Style constraints
- Custom quality criteria

---

## Output Requirements

### Directory Structure

The folder name must match the library's API function name for the plot type:

| Library | Function | Folder Example |
|---------|----------|----------------|
| matplotlib | `ax.boxplot()` | `plots/matplotlib/boxplot/` |
| seaborn | `sns.boxplot()` | `plots/seaborn/boxplot/` |
| plotly | `go.Box()` | `plots/plotly/box/` |
| pygal | `pygal.Box()` | `plots/pygal/box/` |
| altair | `mark_boxplot()` | `plots/altair/boxplot/` |
| plotnine | `geom_boxplot()` | `plots/plotnine/boxplot/` |
| highcharts | `BoxPlotSeries` | `plots/highcharts/boxplot/` |

**Fallback for libraries without native function:** Use `custom/`
- Example: Bokeh has no native boxplot → `plots/bokeh/custom/`

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

    # Save for inspection - ALWAYS use 'plot.png' as filename
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")
```

> **WICHTIG**: Der Ausgabe-Dateiname MUSS immer `plot.png` sein - unabhängig von der
> verwendeten Library (matplotlib, seaborn, plotly). Der Workflow erwartet genau diesen
> Namen. Verwende NIEMALS `test_output_matplotlib.png`, `test_output_seaborn.png` oder
> ähnliche library-spezifische Namen.

### Output Format Requirements

**Current Phase: PNG only**

All plots must output `plot.png`. No HTML, SVG, or interactive outputs.

| Library | PNG Export Method |
|---------|-------------------|
| matplotlib | `plt.savefig('plot.png', dpi=300, bbox_inches='tight')` |
| seaborn | `plt.savefig('plot.png', dpi=300, bbox_inches='tight')` |
| plotly | `fig.write_image('plot.png', width=1000, height=600, scale=2)` |
| bokeh | `export_png(fig, filename='plot.png')` |
| altair | `chart.save('plot.png', scale_factor=2.0)` |
| plotnine | `plot.save('plot.png', dpi=300)` |
| pygal | `chart.render_to_png('plot.png')` |
| highcharts | Selenium screenshot (see example below) |

**Future Phase: Interactive HTML** *(not yet implemented)*
- Interactive plots (HTML) planned for future release
- Will enable hover, zoom, pan for plotly/bokeh/altair
- SVG output also planned for pygal

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

From `docs/workflow.md`:

**Supported Libraries**:
- **matplotlib**: Always implement (universal support)
- **seaborn**: Statistical visualizations (heatmap, violin, box, pair plots, distributions)
- **plotly**: Interactive plots, 3D plots, animations
- **bokeh**: Interactive web-based visualizations
- **altair**: Declarative statistical visualization
- **plotnine**: ggplot2-style plotting (Grammar of Graphics)
- **pygal**: SVG-based charts for web
- **highcharts**: Professional web charts (requires license for commercial use)

**Selection Logic**:
```
if spec mentions "interactive" → plotly, bokeh
else if plot_type in ["heatmap", "violin", "box", "pair"] → seaborn + matplotlib
else if spec mentions "ggplot" or "grammar of graphics" → plotnine
else → all libraries (default)
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
- ✅ Figure size: `figsize=(16, 9)` by default (16:9 aspect ratio)
- ✅ Axis labels: From column names or custom
- ✅ Grid: `ax.grid(True, alpha=0.3)` (subtle)
- ✅ Font sizes: Readable (≥10pt)
- ✅ Legend: If multiple series or color mapping
- ✅ Tight layout: `plt.tight_layout()` to avoid clipping
- ✅ DPI: Always use `dpi=300` when saving for high-quality output

---

## Library-Specific Guidelines

### matplotlib

From `docs/development.md` (lines 332-343):

```python
# Create figure explicitly (16:9 aspect ratio, 300 DPI)
fig, ax = plt.subplots(figsize=(16, 9))

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

### bokeh

```python
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource

# Create figure with categorical x-axis
p = figure(x_range=categories, ...)

# IMPORTANT: For categorical axes, use ColumnDataSource
source = ColumnDataSource(data={'x': cat_data, 'y': num_data})
p.scatter(x='x', y='y', source=source)  # Use scatter, not circle with categorical

# Save output
output_file('plot.html')
save(p)

# PNG export (requires selenium)
try:
    from bokeh.io import export_png
    export_png(p, filename='plot.png')
except ImportError:
    print("Note: Install 'selenium' for PNG export")
```

### altair

```python
import altair as alt

# Create chart
chart = alt.Chart(data).mark_point().encode(x='x:Q', y='y:Q')

# Save HTML (always works)
chart.save('plot.html')

# PNG export (requires vl-convert-python)
try:
    chart.save('plot.png', scale_factor=2.0)
except Exception:
    print("Note: Install 'vl-convert-python' for PNG export")
```

### plotnine

```python
from plotnine import ggplot, aes, scale_fill_brewer

# IMPORTANT: Palette types must match the palette name
# - Qualitative: Set1, Set2, Set3, Paired, Pastel1, Pastel2, Dark2, Accent
# - Sequential: Blues, Greens, Reds, Oranges, Purples, Greys, etc.
# - Diverging: RdBu, PiYG, PRGn, BrBG, RdYlBu, etc.

# ✅ Correct: Set2 is qualitative
+ scale_fill_brewer(type='qual', palette='Set2')

# ❌ Wrong: Set2 is NOT sequential
+ scale_fill_brewer(type='seq', palette='Set2')
```

### highcharts

**Note:** Highcharts requires a license for commercial use.

```python
# IMPORTANT: Use correct import path
from highcharts_core.chart import Chart  # ✅ Correct
# NOT: from highcharts_core import Chart  # ❌ Wrong

from highcharts_core.options import HighchartsOptions

# Create chart
chart = Chart()
chart.options = HighchartsOptions()

# Export to HTML (always works)
html_str = chart.to_js_literal()

# Static image export requires Highcharts Export Server
```

### pygal

```python
import pygal

# Create chart
chart = pygal.Bar()
chart.title = 'Title'
chart.add('Series', [1, 2, 3])

# Save as SVG (native format)
chart.render_to_file('plot.svg')

# PNG export (requires cairosvg)
try:
    chart.render_to_png('plot.png')
except ImportError:
    print("Note: Install 'cairosvg' for PNG export")
```

---

## API Version Compatibility

### matplotlib 3.9+

```python
# DEPRECATED: labels parameter in boxplot
ax.boxplot(data, labels=group_names)  # ❌ Deprecated

# USE: tick_labels parameter
ax.boxplot(data, tick_labels=group_names)  # ✅ Correct
```

### seaborn 0.14+

```python
# When using palette, always specify hue
# Otherwise seaborn raises a warning

# ❌ Warning: palette without hue
sns.boxplot(data=df, x='group', y='value', palette='Set2')

# ✅ Correct: hue with palette
sns.boxplot(data=df, x='group', y='value', hue='group', palette='Set2', legend=False)
```

---

## Code Quality Checks (Required Before PR)

Before creating a pull request, **always** run these checks and fix any issues:

```bash
# 1. Check for linting issues
uv run ruff check .

# 2. Auto-fix issues (safe fixes)
uv run ruff check . --fix

# 3. Auto-fix with unsafe fixes if needed
uv run ruff check . --fix --unsafe-fixes

# 4. Format code
uv run ruff format .
```

**Common issues to watch for:**
- `C408`: Use dict literals `{}` instead of `dict()`
- `B905`: Add `strict=False` to `zip()` calls
- `B007`: Prefix unused loop variables with `_` (e.g., `_group`)
- Import ordering (auto-fixed by ruff)

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
