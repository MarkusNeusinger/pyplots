# line-basic: Basic Line Chart

A fundamental line chart that visualizes trends and patterns in data over a continuous axis, typically time or sequential values.

## Data Requirements

- **x**: Numeric or temporal column for x-axis values (typically time or sequence)
- **y**: Numeric column for y-axis values

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `color`: Line color (default: "steelblue")
- `linewidth`: Width of the line (default: 2)
- `marker`: Marker style for data points (default: None)
- `marker_size`: Size of markers if enabled (default: 6)
- `alpha`: Transparency level for the line (default: 1.0)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `linestyle`: Line style (default: "solid")

## Expected Output

A line chart with:
- X and Y axes labeled with column names (or custom labels)
- Smooth connected line through all data points
- Grid visible but subtle (alpha <= 0.3)
- Professional appearance with proper spacing
- Clear trend visualization

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Line clearly visible with appropriate width
- [x] No overlapping labels
- [x] Appropriate figure size (16:9 aspect ratio)
- [x] Type hints and validation present
- [x] Data accurately represented

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'month': [1, 2, 3, 4, 5, 6],
    'sales': [100, 150, 130, 180, 200, 190]
})
fig = create_plot(data, 'month', 'sales')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'month',
    'sales',
    color='darkblue',
    linewidth=3,
    title='Monthly Sales Trend',
    marker='o'
)
```

## Tags

line, trend, timeseries, basic, 2d

## Use Cases

- Tracking sales or revenue trends over time
- Visualizing stock price movements
- Displaying temperature changes throughout a period
- Monitoring website traffic or user engagement metrics
- Showing project progress over time

## Implementation Notes

- Sort data by x-axis values to ensure proper line connections
- Handle missing/NaN values gracefully
- Validate that columns contain numeric data
