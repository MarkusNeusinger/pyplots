# area-basic: Basic Area Chart

A fundamental area chart that visualizes data as a filled region between the line and the axis, ideal for showing magnitude and trends over time or ordered categories.

## Data Requirements

- **x**: Numeric or categorical column for x-axis values (often time or sequence)
- **y**: Numeric column for y-axis values (the values to plot)

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `alpha`: Transparency level for fill (default: 0.5)
- `color`: Fill color (default: "steelblue")
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `line_color`: Color of the line on top of area (default: same as color)
- `line_width`: Width of the line (default: 2)

## Expected Output

An area chart with:
- X and Y axes labeled with column names (or custom labels)
- Filled area between the line and the x-axis
- Visible line on top of the filled area
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing
- Smooth transitions between data points

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Area fill clearly visible with appropriate transparency
- [x] Line visible on top of area
- [x] No overlapping labels
- [x] Appropriate figure size
- [x] Type hints and validation present

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'month': [1, 2, 3, 4, 5, 6],
    'sales': [100, 150, 130, 180, 200, 220]
})
fig = create_plot(data, 'month', 'sales')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'month',
    'sales',
    alpha=0.3,
    color='green',
    title='Monthly Sales'
)
```

## Implementation Notes

- Use appropriate alpha value for fill visibility
- Ensure the line is visible above the filled area
- Handle missing/NaN values gracefully
- Validate that y column contains numeric data

## Tags

area, trend, time-series, basic, 2d

## Use Cases

- Visualizing stock price trends over time
- Showing website traffic patterns by hour or day
- Displaying cumulative sales or revenue data
- Monitoring resource usage (CPU, memory) over time
