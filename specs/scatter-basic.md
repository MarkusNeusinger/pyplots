# scatter-basic: Basic Scatter Plot

A fundamental scatter plot that visualizes the relationship between two continuous variables, optimized for handling many data points.

## Data Requirements

- **x**: Numeric column for x-axis values
- **y**: Numeric column for y-axis values

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `alpha`: Transparency level for points (default: 0.6 for better visibility with many points)
- `size`: Point size (default: 30)
- `color`: Point color (default: "steelblue")
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `edgecolors`: Edge color for points (default: None)
- `linewidth`: Width of edge lines (default: 0)

## Expected Output

A scatter plot with:
- X and Y axes labeled with column names (or custom labels)
- Consistent point color and size
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing
- Optimized for displaying many points without excessive overplotting

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Points clearly visible even with many data points
- [x] No overlapping labels
- [x] Appropriate alpha for density visualization
- [x] Appropriate figure size
- [x] Type hints and validation present

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 6]
})
fig = create_plot(data, 'x', 'y')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'x',
    'y',
    alpha=0.5,
    size=20,
    title='Data Distribution',
    color='darkblue'
)
```

## Implementation Notes

- Use appropriate alpha value for handling overlapping points
- Ensure plot is readable even with thousands of points
- Handle missing/NaN values gracefully
- Validate that x and y columns contain numeric data