# line-basic: Basic Line Chart

**Spec Version:** 1.0.0

## Description

A fundamental line chart that displays data points connected by straight line segments. Ideal for visualizing trends over time or ordered categories, showing the progression and direction of data values.

## Data Requirements

- **x**: Numeric or datetime column for x-axis values (typically representing time or sequence)
- **y**: Numeric column for y-axis values (the measurement or metric)

## Optional Parameters

- `figsize`: Figure size as (width, height) tuple (default: (16, 9))
- `color`: Line color (default: "steelblue")
- `linewidth`: Width of the line (default: 2.0)
- `marker`: Marker style for data points (default: "o")
- `markersize`: Size of markers (default: 6)
- `alpha`: Transparency level (default: 0.8)
- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `linestyle`: Line style (default: "-" solid)

## Quality Criteria

- [x] X and Y axes are labeled with column names or custom labels
- [x] Line clearly visible with appropriate width and color
- [x] Grid visible but subtle (alpha ≤ 0.3)
- [x] No overlapping axis labels or tick marks
- [x] Data points optionally marked for clarity
- [x] Appropriate figure size (16:9 aspect ratio)
- [x] Type hints and validation present

## Expected Output

A clean line chart with data points connected by a continuous line. The plot should have clearly labeled axes, a subtle grid for readability, and optionally markers at each data point. The line should be clearly visible against the background, with sufficient contrast. The overall design should be professional and minimal, suitable for reports and presentations.

## Tags

line, trend, timeseries, basic, 2d

## Use Cases

- Tracking monthly sales figures over a year
- Visualizing stock price movements over time
- Monitoring temperature changes throughout a day
- Displaying website traffic trends over weeks
- Showing progress of a metric over time
