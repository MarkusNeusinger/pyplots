# line-basic: Basic Line Chart

A simple line chart that connects data points to visualize trends and changes over a sequence, commonly used for time series or ordered categorical data.

## Data Requirements

- **x**: Column for x-axis values (numeric, datetime, or categorical)
- **y**: Numeric column for y-axis values

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (10, 6))
- `color`: Line color (default: "steelblue")
- `linewidth`: Width of the line (default: 2)
- `marker`: Marker style for data points (default: "o")
- `markersize`: Size of markers (default: 6)
- `alpha`: Transparency level (default: 1.0)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)

## Expected Output

A line chart with:
- X and Y axes labeled with column names (or custom labels)
- Single line connecting data points in order
- Optional markers at each data point
- Grid visible but subtle (alpha <= 0.3)
- Professional appearance with clean, minimal design
- Readable axis labels and tick marks

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Line clearly visible with appropriate width
- [x] No overlapping labels
- [x] Data points connected in correct order
- [x] Appropriate figure size
- [x] Type hints and validation present

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'sales': [100, 120, 90, 140, 160]
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
    marker='s',
    title='Monthly Sales'
)
```

## Implementation Notes

- Ensure data points are connected in the order they appear in the DataFrame
- Handle missing/NaN values gracefully (consider interpolation or gaps)
- Line should be clearly visible against the background
- Markers help identify individual data points

## Use Cases

- Tracking monthly sales or revenue over time
- Monitoring temperature changes throughout the day
- Visualizing stock price movements
- Displaying website traffic trends
- Showing progress metrics over project timeline
