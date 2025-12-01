# area-basic: Basic Area Chart

A simple filled area chart showing a single data series over time or sequential x-values, emphasizing the magnitude of values through the filled region below the line.

## Data Requirements

- **x**: Numeric or datetime column for x-axis values (sequential or time-based)
- **y**: Numeric column for y-axis values (the area will be filled from zero to this value)

## Optional Parameters

- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `color`: Fill color for the area (default: "steelblue")
- `alpha`: Transparency level for the fill (default: 0.7)
- `line_color`: Color of the line at the top of the area (default: same as fill color)
- `line_width`: Width of the top line (default: 2)
- `show_line`: Whether to show the line at the top of the area (default: True)

## Expected Output

A filled area chart with:
- X and Y axes labeled with column names (or custom labels)
- Filled area from zero (baseline) to the data values
- Optional line at the top edge of the filled area
- Grid visible but subtle (alpha ≤ 0.3)
- Professional appearance with proper spacing
- Smooth visual representation of trends with emphasis on magnitude

## Quality Criteria

- [x] Axes labeled clearly
- [x] Grid visible but subtle
- [x] Fill area clearly visible with appropriate transparency
- [x] No overlapping labels
- [x] Appropriate figure size (16:9 aspect ratio)
- [x] Type hints and validation present
- [x] Colorblind-safe default color

## Examples

### Example 1: Basic Usage
```python
import pandas as pd
data = pd.DataFrame({
    'month': [1, 2, 3, 4, 5, 6],
    'sales': [100, 150, 200, 180, 220, 250]
})
fig = create_plot(data, 'month', 'sales')
```

### Example 2: Custom Styling
```python
fig = create_plot(
    data,
    'month',
    'sales',
    alpha=0.5,
    title='Monthly Sales Trend',
    color='teal'
)
```

## Use Cases

- Visualizing cumulative values over time (e.g., total revenue growth)
- Showing trends with emphasis on magnitude (e.g., stock prices)
- Comparing values to a baseline (e.g., temperature variations from average)
- Displaying time series data where the area under the curve is meaningful
- Illustrating resource utilization over time (e.g., CPU usage)

## Tags

area, trend, time-series, basic, 2d
