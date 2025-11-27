# scatter-color-groups: Scatter Plot with Color Groups

A scatter plot that visualizes data points colored by categorical groups, showing distinct "color clouds" for different categories in a 2D x-y space.

## Data Requirements

- **x**: Numeric column for x-axis values
- **y**: Numeric column for y-axis values
- **group**: Categorical column defining which color group each point belongs to

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `alpha`: Transparency level for points (default: 0.7)
- `size`: Point size (default: 50)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `palette`: Color palette name (default: "Set1")

## Expected Output

A scatter plot with:
- X and Y axes labeled with column names (or custom labels)
- Different colors for each categorical group
- Legend showing group-to-color mapping
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Points clearly distinguishable
- [x] No overlapping labels
- [x] Legend present and readable
- [x] Colorblind-safe palette
- [x] Appropriate figure size
- [x] Type hints and validation present

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 6],
    'y': [2, 4, 3, 5, 6, 4],
    'group': ['A', 'A', 'B', 'B', 'C', 'C']
})
fig = create_plot(data, 'x', 'y', 'group')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'x',
    'y',
    'group',
    alpha=0.8,
    size=100,
    title='Sales by Region',
    palette='husl'
)
```

## Implementation Notes

- Use distinct, colorblind-safe colors for groups
- Ensure all group values fit in legend without overlap
- Handle missing/NaN values gracefully
- Validate that group column contains categorical data
