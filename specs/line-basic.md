# line-basic: Basic Line Plot

A fundamental line plot that visualizes trends and changes in data over a continuous or sequential axis, commonly used for time series and ordered data.

## Data Requirements

- **x**: Column for x-axis values (numeric, datetime, or ordered categorical)
- **y**: Numeric column for y-axis values

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (16, 9))
- `color`: Line color (default: "steelblue")
- `linewidth`: Width of the line (default: 2.0)
- `linestyle`: Line style, e.g., '-', '--', '-.', ':' (default: '-')
- `marker`: Marker style for data points (default: None)
- `markersize`: Size of markers (default: 6)
- `alpha`: Transparency level (default: 1.0)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)

## Expected Output

A line plot with:
- X and Y axes labeled with column names (or custom labels)
- Smooth, continuous line connecting data points
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing
- Optional markers at data points for clarity

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Line clearly visible with appropriate width
- [x] No overlapping labels
- [x] Appropriate figure size (16:9 aspect ratio)
- [x] Type hints and validation present
- [x] Data sorted by x-axis for proper line rendering

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'time': [1, 2, 3, 4, 5],
    'value': [2, 4, 3, 5, 6]
})
fig = create_plot(data, 'time', 'value')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'time',
    'value',
    color='darkblue',
    linewidth=2.5,
    marker='o',
    title='Trend Analysis'
)
```

## Implementation Notes

- Data should be sorted by x-axis values for proper line rendering
- Handle missing/NaN values gracefully
- Validate that y column contains numeric data
- X-axis can be numeric, datetime, or ordered categorical

## Tags

line, trend, time-series, basic, 2d

## Use Cases

- Time series visualization of stock prices
- Tracking metrics over time (e.g., website traffic)
- Displaying trends in scientific measurements
- Monitoring system performance metrics
- Visualizing growth or decline patterns
