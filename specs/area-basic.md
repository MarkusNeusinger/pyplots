# area-basic: Basic Area Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
-->

**Spec Version:** 1.0.0

## Description

Create a simple area chart showing a filled region between the x-axis and a line.
Perfect for visualizing quantities over continuous intervals, trends over time, or cumulative values.
Works with any dataset containing a continuous x variable and numeric y values.

## Data Requirements

- **x**: Values for the x-axis (numeric or datetime: continuous sequence)
- **y**: Numeric values defining the top of the filled area (numeric: continuous values)

## Optional Parameters

- `color`: Fill color for the area (type: string, default: "steelblue")
- `alpha`: Transparency level for the filled area (type: float 0.0-1.0, default: 0.4)
- `line_color`: Color of the top edge line (type: string, default: same as fill color)
- `line_width`: Width of the top edge line (type: float, default: 2.0)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (16, 9))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3
- [ ] Filled area is clearly visible with appropriate transparency
- [ ] Top edge line is visible and distinguishes the data boundary
- [ ] No overlapping axis labels or tick marks
- [ ] Colorblind-safe colors (use accessible defaults)
- [ ] Appropriate figure size (16x9 default) for readability
- [ ] Title is centered and clearly readable if provided (fontsize 14, bold)

## Expected Output

A clean area chart with a filled region extending from the x-axis up to the data values.
The filled area should have moderate transparency to show grid lines underneath while remaining clearly visible.
A solid line along the top edge should clearly define where the data values lie.
The plot should be immediately understandable without additional explanation.
All text elements (labels, title, and tick labels) should be legible at standard display sizes.

## Tags

trend, continuous, basic, area, time-series, statistical, exploratory

## Use Cases

- Stock price visualization showing value over time (e.g., daily closing prices)
- Website traffic metrics over time (e.g., daily page views)
- Temperature variations throughout a day or season
- Revenue or sales trends over months or years
- Resource utilization over time (e.g., CPU usage, memory consumption)
- Population growth over time periods
