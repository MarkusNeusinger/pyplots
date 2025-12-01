# line-basic: Basic Line Plot

**Spec Version:** 1.0.0

## Description

A fundamental line plot that visualizes trends over continuous or sequential data. Ideal for showing how values change over time or across ordered categories, connecting data points with straight line segments.

## Data Requirements

- **x**: Numeric or datetime column for x-axis values (typically time or sequence)
- **y**: Numeric column for y-axis values

## Optional Parameters

- `title`: Plot title (type: str, default: None)
- `xlabel`: X-axis label (type: str, default: column name)
- `ylabel`: Y-axis label (type: str, default: column name)
- `color`: Line color (type: str, default: "steelblue")
- `line_width`: Width of the line (type: float, default: 2.0)
- `marker`: Marker style for data points (type: str, default: None)
- `marker_size`: Size of markers if enabled (type: float, default: 8)
- `alpha`: Line transparency (type: float, default: 1.0)

## Quality Criteria

- [ ] X and Y axes are labeled with column names or custom labels
- [ ] Grid is visible but subtle (alpha <= 0.3)
- [ ] Line is clearly visible with appropriate width
- [ ] No overlapping axis labels or tick marks
- [ ] Data points are connected in correct order
- [ ] Figure uses 16:9 aspect ratio
- [ ] Type hints and input validation present

## Expected Output

A line plot with data points connected by line segments. The x-axis represents the independent variable (often time or sequence), and the y-axis represents the dependent variable being measured. The line should be clearly visible against the grid background, with proper axis labels and title (if provided). The plot should handle various data sizes gracefully and maintain readability.

## Tags

line, trend, time-series, basic, 2d

## Use Cases

- Tracking stock prices over time
- Monitoring temperature changes throughout the day
- Displaying website traffic over months
- Showing sales growth across quarters
- Visualizing sensor readings over time
- Analyzing experiment results over sequential trials
