# Code Generation Rules v{VERSION}

## Metadata
- **Version**: {VERSION} (e.g., "1.0.0")
- **Type**: Generation
- **Status**: {STATUS} (draft/active/deprecated/archived)
- **Last Updated**: {DATE}
- **Author**: {AUTHOR}

## Purpose

Define how AI generates plot implementation code from specifications.

**Goal**: Produce high-quality, executable, well-documented Python code that implements the spec requirements.

---

## Input Format

### Required Inputs
1. **Spec Markdown**: Complete spec file from `specs/{spec-id}.md`
2. **Target Library**: Which plotting library to use (matplotlib, seaborn, plotly, etc.)
3. **Variant**: Which implementation variant (default, style-specific, version-specific)

### Optional Inputs
- Python version target (e.g., "3.12")
- Style constraints (colors, figure size, etc.)
- Custom quality criteria

---

## Output Requirements

### File Structure

```python
"""
{spec-id}: {Spec Title}
Implementation for: {library}
Variant: {variant}
Python: {python_version}+
"""

import {required_libraries}
import pandas as pd
from {typing} import {types}


def create_plot(
    data: pd.DataFrame,
    {required_params}: {types},
    {optional_params}: {types} = {defaults},
    **kwargs
) -> {return_type}:
    """
    {Brief description}

    Args:
        data: {Description}
        {param}: {Description}
        **kwargs: Additional parameters passed to {underlying_function}

    Returns:
        {Description of return value}

    Raises:
        {Exception}: {When it's raised}

    Example:
        >>> {example_code}
    """
    # Validation
    {validation_code}

    # Create plot
    {plotting_code}

    # Styling
    {styling_code}

    return {result}


# Optional: Standalone execution for testing
if __name__ == '__main__':
    # Sample data
    {sample_data}

    # Create plot
    {create_plot_call}

    # Save or show
    {save_or_show}
```

---

## Generation Process

### Step 1: Analyze Spec

**Actions**:
1. Read entire spec Markdown file
2. Extract data requirements (required parameters)
3. Extract optional parameters with defaults
4. Understand expected output description
5. Review quality criteria checklist
6. Note use cases for context

**Key Points**:
- Identify parameter types (numeric, categorical, datetime)
- Understand relationships (e.g., "x vs y", "group by category")
- Note any special requirements (colorblind-safe, specific dimensions)

### Step 2: Plan Implementation

**Decisions**:
1. **Library Selection**:
   - {LIBRARY_SELECTION_RULES}

2. **Plot Type Mapping**:
   - {PLOT_TYPE_MAPPING}

3. **Data Structure**:
   - {DATA_STRUCTURE_DECISIONS}

4. **Styling Approach**:
   - {STYLING_APPROACH}

### Step 3: Generate Code

**Code Structure** (in order):

1. **Module Docstring**:
   ```python
   """
   {spec-id}: {title}
   Implementation for: {library}
   """
   ```

2. **Imports**:
   ```python
   # Standard library (if needed)
   from typing import ...

   # Third-party (plotting library)
   import {library}
   import pandas as pd

   # Local (if needed)
   # from core.utils import ...
   ```

3. **Function Definition**:
   ```python
   def create_plot(
       data: pd.DataFrame,
       # Required parameters from spec
       {required_params}: {types},
       # Optional parameters from spec
       {optional_params}: {types} = {defaults},
       # Catch-all for library-specific options
       **kwargs
   ) -> {return_type}:
   ```

4. **Docstring** (Google style):
   ```python
   """
   {One-line summary}

   {Longer description if needed}

   Args:
       data: {Description}
       {param}: {Description}

   Returns:
       {Description}

   Raises:
       {Exception}: {Condition}

   Example:
       >>> {code}
   """
   ```

5. **Validation**:
   ```python
   # Check data not empty
   if data.empty:
       raise ValueError("Data cannot be empty")

   # Check required columns exist
   if {param} not in data.columns:
       raise KeyError(f"Column '{{{param}}}' not found")

   # Check data types if needed
   # Check value ranges if needed
   ```

6. **Main Plotting Logic**:
   ```python
   # Create figure/axes
   {create_figure}

   # Plot data
   {plot_calls}

   # Styling
   {styling}

   # Labels and title
   {labels}

   return {figure}
   ```

7. **Standalone Execution Block** (optional):
   ```python
   if __name__ == '__main__':
       # Sample data
       data = {sample}

       # Generate plot
       fig = create_plot(data, ...)

       # Save/show
       plt.savefig('test.png')
   ```

### Step 4: Apply Quality Standards

**Code Quality**:
- ✅ Type hints on all parameters and return
- ✅ Complete docstrings (Google style)
- ✅ Input validation
- ✅ Clear error messages
- ✅ Consistent naming (snake_case)
- ✅ Max line length: 120 characters
- ✅ No hardcoded values (use parameters)

**Visual Quality**:
- ✅ Appropriate figure size (default: 10x6 inches)
- ✅ Clear axis labels (from column names or custom)
- ✅ Readable font sizes (minimum 10pt)
- ✅ Subtle grid (alpha ≤ 0.5)
- ✅ Legend if multiple series
- ✅ Title if provided
- ✅ Tight layout to avoid clipping

---

## Library-Specific Guidelines

### matplotlib

**Best Practices**:
```python
# Create figure and axes explicitly
fig, ax = plt.subplots(figsize=(10, 6))

# Use axes methods (not pyplot)
ax.scatter(...)  # ✅ Good
plt.scatter(...) # ❌ Avoid

# Grid configuration
ax.grid(True, alpha=0.3, linestyle='--')

# Tight layout
plt.tight_layout()

# Return figure
return fig
```

### seaborn

**Best Practices**:
```python
# Set style if needed
sns.set_style("whitegrid")

# Use seaborn's high-level API
fig = sns.scatterplot(data=data, x=x, y=y)

# Get underlying matplotlib figure
fig = plt.gcf()

return fig
```

### plotly

**Best Practices**:
```python
import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(...))

# Update layout
fig.update_layout(
    title=title,
    xaxis_title=x,
    yaxis_title=y
)

return fig
```

---

## Example

### Input Spec Excerpt

```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Data Requirements
- **x**: Numeric values for x-axis
- **y**: Numeric values for y-axis

## Optional Parameters
- `color`: Point color or column name
- `size`: Point size (default: 50)
- `alpha`: Transparency (default: 0.8)
```

### Generated Code

```python
"""
scatter-basic-001: Basic 2D Scatter Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: float = 50,
    alpha: float = 0.8,
    title: str | None = None,
    **kwargs
) -> Figure:
    """
    Create a basic 2D scatter plot

    Args:
        data: Input DataFrame
        x: Column name for x-axis
        y: Column name for y-axis
        color: Point color or column for color mapping
        size: Point size in pixels (default: 50)
        alpha: Transparency 0-1 (default: 0.8)
        title: Plot title (optional)
        **kwargs: Additional parameters for ax.scatter()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If x or y column not found

    Example:
        >>> data = pd.DataFrame({'x': [1,2,3], 'y': [2,4,6]})
        >>> fig = create_plot(data, x='x', y='y')
    """
    # Validation
    if data.empty:
        raise ValueError("Data cannot be empty")
    if x not in data.columns:
        raise KeyError(f"Column '{x}' not found")
    if y not in data.columns:
        raise KeyError(f"Column '{y}' not found")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot
    scatter_kwargs = {'s': size, 'alpha': alpha, **kwargs}

    if color and color in data.columns:
        # Color mapping
        scatter = ax.scatter(data[x], data[y], c=data[color], **scatter_kwargs)
        plt.colorbar(scatter, ax=ax, label=color)
    else:
        # Single color
        scatter_kwargs['color'] = color or 'blue'
        ax.scatter(data[x], data[y], **scatter_kwargs)

    # Styling
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
```

---

## Quality Checklist

Before considering generation complete, verify:

- [ ] Code executes without errors
- [ ] All spec requirements implemented
- [ ] Type hints present and correct
- [ ] Docstring complete (Args, Returns, Raises, Example)
- [ ] Input validation included
- [ ] Error messages are clear
- [ ] Code is readable and well-formatted
- [ ] No hardcoded magic numbers
- [ ] Returns correct type
- [ ] Standalone execution block works

---

## Common Pitfalls

### ❌ Avoid

**1. Missing Validation**:
```python
def create_plot(data, x, y):
    # ❌ No validation!
    return ax.scatter(data[x], data[y])
```

**2. Poor Error Messages**:
```python
if x not in data.columns:
    raise KeyError("Not found")  # ❌ What's not found?
```

**3. Hardcoded Values**:
```python
ax.scatter(data[x], data[y], s=50)  # ❌ Should be parameter
```

**4. Incomplete Docstrings**:
```python
def create_plot(data, x, y):
    """Create plot"""  # ❌ Too brief
```

### ✅ Best Practices

```python
def create_plot(
    data: pd.DataFrame,  # ✅ Type hints
    x: str,
    y: str,
    size: float = 50     # ✅ Parameterized
) -> Figure:             # ✅ Return type
    """
    Create scatter plot  # ✅ Complete docstring

    Args:
        data: Input DataFrame
        x: Column for x-axis
        y: Column for y-axis
        size: Point size (default: 50)

    Returns:
        Matplotlib Figure

    Raises:
        KeyError: If columns not found
    """
    # ✅ Validation
    if x not in data.columns:
        raise KeyError(f"Column '{x}' not found in {list(data.columns)}")

    # Plot logic...
```

---

## Notes for Implementers

### When to Create New Version

Create a new version when you change:
- Code structure requirements
- Validation rules
- Docstring format
- Quality standards
- Library-specific guidelines

### Customization Points

You can customize this template for specific needs:
- **Project-specific**: Add company style guide requirements
- **Library-specific**: Add more detailed library guidelines
- **Domain-specific**: Add domain requirements (e.g., scientific, financial)

### Testing

Always test generated code:
1. Execute with sample data
2. Check all quality criteria
3. Verify edge cases (empty data, missing columns, etc.)

---

## Related Documents

- [Quality Criteria Template](./quality-criteria-template.md)
- [Evaluation Prompt Template](./evaluation-prompt-template.md)
- [Rule Versioning Guide](../../docs/architecture/rule-versioning.md)

---

*Fill in {PLACEHOLDERS} when creating a new version*
