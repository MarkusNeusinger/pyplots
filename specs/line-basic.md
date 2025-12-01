# line-basic: Basic Line Plot

A fundamental line plot that visualizes trends and changes in data over a continuous variable, typically time or ordered categories.

## Data Requirements

- **x**: Column for x-axis values (numeric, datetime, or ordered categorical)
- **y**: Numeric column for y-axis values

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `color`: Line color (default: "steelblue")
- `linewidth`: Width of the line (default: 2)
- `marker`: Marker style for data points (default: None)
- `marker_size`: Size of markers (default: 6)
- `alpha`: Line transparency (default: 1.0)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `show_dots`: Whether to show data point markers (default: True)

## Expected Output

A line plot with:
- X and Y axes labeled with column names (or custom labels)
- Smooth, continuous line connecting data points
- Optional markers at each data point
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing
- Clear visualization of trends and patterns

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Line clearly visible with appropriate width
- [x] No overlapping labels
- [x] Markers (if shown) are appropriately sized
- [x] Appropriate figure size
- [x] Type hints and validation present

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'month': [1, 2, 3, 4, 5, 6],
    'sales': [100, 120, 115, 140, 160, 155]
})
fig = create_plot(data, 'month', 'sales')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'month',
    'sales',
    title='Monthly Sales Trend',
    color='darkgreen',
    linewidth=2.5,
    show_dots=True
)
```

## Implementation Notes

- Ensure data is sorted by x-axis values for proper line rendering
- Handle missing/NaN values gracefully
- Validate that y column contains numeric data
- Use appropriate line width for visibility

## Tags

line, trend, basic, time-series

## Use Cases

- Tracking stock prices over time
- Monitoring temperature changes throughout a day
- Visualizing sales trends over months or years
- Displaying performance metrics over iterations
- Showing population growth over decades
