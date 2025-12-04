# line-basic: Basic Line Plot

A fundamental line plot for visualizing trends and continuous data over an ordered sequence. Ideal for time series, trend analysis, and any scenario where data points should be connected to show progression or change over time.

## Description

A basic line plot connects data points with a continuous line to reveal trends, patterns, and changes in data over a sequence. This is one of the most common visualization types, essential for time series analysis, tracking metrics over time, and showing how values evolve across ordered categories or indices.

## Data Requirements

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| x | numeric/datetime | Yes | X-axis values representing the sequence (time, index, or ordered category) |
| y | numeric | Yes | Y-axis values representing the measured quantity |

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| figsize | tuple | (10, 6) | Figure size as (width, height) in inches |
| linewidth | float | 2.0 | Width of the line in points |
| color | string | "steelblue" | Line color |
| alpha | float | 1.0 | Line transparency (0.0 to 1.0) |
| marker | string | None | Marker style for data points (e.g., 'o', 's', '^') |
| markersize | float | 6.0 | Size of markers if enabled |
| title | string | "Line Plot" | Plot title |
| xlabel | string | "X" | X-axis label |
| ylabel | string | "Y" | Y-axis label |
| linestyle | string | "-" | Line style ('-', '--', '-.', ':') |
| grid | bool | True | Whether to show grid lines |

## Quality Criteria

- [ ] X and Y axes are clearly labeled with descriptive text
- [ ] Line is clearly visible with appropriate width (2px or equivalent)
- [ ] Grid lines are visible but subtle (alpha ≤ 0.3) for readability
- [ ] No overlapping axis labels or tick marks
- [ ] Data points are accurately connected in sequential order
- [ ] Figure size is appropriate (10x6 inches or equivalent aspect ratio)
- [ ] Title is present and descriptive
- [ ] Line color provides good contrast against background
- [ ] Type hints and input validation are present in implementation
- [ ] Handles edge cases gracefully (empty data, single point, NaN values)

## Expected Output

A clean, professional line plot with a single continuous line connecting all data points in order. The plot should have:
- A clear title at the top ("Line Plot" by default)
- Labeled X and Y axes with appropriate tick marks
- A subtle grid for easy value reading
- Sufficient margins so no labels are cut off
- A line width of 2px (or equivalent) for good visibility
- Optional markers at data points for precise value identification

The overall appearance should be minimal and professional, suitable for reports, presentations, and dashboards.

## Tags

line, trend, time-series, basic, 2d, sequential

## Use Cases

- **Stock price tracking**: Visualizing daily closing prices of a stock over weeks or months to identify trends and patterns
- **Temperature monitoring**: Plotting daily average temperatures over a year to see seasonal variations
- **Website analytics**: Showing daily page views or unique visitors over time to track growth or detect anomalies
- **Sales progression**: Displaying monthly or quarterly sales figures to identify business trends
- **Performance metrics**: Tracking application response times or system CPU usage over time
- **Scientific measurements**: Plotting experimental readings taken at regular intervals during an experiment

## Example Data

```python
import pandas as pd

data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'y': [2.3, 3.1, 4.5, 4.2, 5.8, 6.1, 5.9, 7.2, 8.1, 7.8]
})

fig = create_plot(data, 'x', 'y')
```

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

### Example 2: Custom Styling with Markers
```python
fig = create_plot(
    data,
    'x',
    'y',
    linewidth=2.5,
    marker='o',
    markersize=8,
    title='Monthly Sales Trend',
    xlabel='Month',
    ylabel='Sales ($)',
    color='darkgreen'
)
```

### Example 3: Time Series Data
```python
import pandas as pd

data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'value': [23, 25, 22, 28, 30, 29, 31, 33, 32, 35,
              34, 36, 38, 37, 40, 42, 41, 43, 45, 44,
              46, 48, 47, 50, 52, 51, 53, 55, 54, 56]
})
fig = create_plot(data, 'date', 'value', title='Daily Metrics')
```

## Implementation Notes

- Sort data by x-axis values before plotting to ensure correct line connectivity
- Handle missing/NaN values gracefully (skip or interpolate based on library capabilities)
- Validate that x and y columns exist and contain appropriate data types
- Use antialiasing for smooth line rendering where supported
- Ensure consistent behavior across all 9 supported libraries
