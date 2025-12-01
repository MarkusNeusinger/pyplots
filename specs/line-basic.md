# line-basic: Basic Line Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
-->

**Spec Version:** 1.0.0

## Description

Create a simple line chart connecting data points in order, ideal for showing trends and continuous data over a sequence.
Perfect for visualizing time series data, tracking changes over intervals, and displaying relationships between ordered data points.
Works with any dataset containing sequential x-values (numeric or categorical) and corresponding y-values.

## Data Requirements

- **x**: Sequential values for the x-axis (numeric or categorical: represents order, time, or sequence index)
- **y**: Numeric values for the y-axis (numeric: continuous values to be plotted)

## Optional Parameters

- `color`: Line color (type: string, default: "steelblue")
- `linewidth`: Line thickness (type: float, default: 2.0)
- `marker`: Marker style at data points (type: string or None, default: None)
- `marker_size`: Size of markers if shown (type: float, default: 6)
- `alpha`: Line transparency (type: float 0.0-1.0, default: 1.0)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (10, 6))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3
- [ ] Line is clearly visible with appropriate width (minimum 1.5px)
- [ ] No overlapping axis labels or tick marks
- [ ] Appropriate figure size (10x6 inches default) for readability
- [ ] Title is centered and clearly readable if provided (fontsize 14, bold)
- [ ] Data points are connected in correct order
- [ ] Line color provides good contrast against white background

## Expected Output

A clean line chart with a single line connecting data points in sequence.
The plot should clearly show the trend or pattern in the data.
Grid lines should help with reading values without overpowering the data.
The x-axis should show the sequence values and the y-axis should show the corresponding numeric values.
All text elements (labels, title, and tick labels) should be legible at standard display sizes.

## Tags

line, trend, timeseries, basic, sequential, continuous, exploratory

## Use Cases

- Stock price movement over time (e.g., daily closing prices)
- Temperature changes throughout the day (e.g., hourly readings)
- Website traffic over time (e.g., daily page views)
- Sales performance tracking (e.g., monthly revenue)
- Sensor data visualization (e.g., continuous measurements)
- Progress tracking (e.g., project completion over weeks)
