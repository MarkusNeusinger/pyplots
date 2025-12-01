# area-basic: Basic Area Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
-->

**Spec Version:** 1.0.0

## Description

Create a simple filled area chart showing a single data series over time or sequential x-values.
Perfect for visualizing cumulative values, trends with emphasis on magnitude, and comparing values to a baseline.
Works with any dataset containing sequential x-values and numeric y-values.

## Data Requirements

- **x**: Sequential values for x-axis (datetime, numeric, or categorical)
- **y**: Numeric values representing the area height at each x point

## Optional Parameters

- `color`: Fill color for the area (type: string, default: "steelblue")
- `alpha`: Transparency level for fill (type: float 0.0-1.0, default: 0.4)
- `line_alpha`: Transparency level for edge line (type: float 0.0-1.0, default: 1.0)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (16, 9))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3
- [ ] Area fill is clearly visible with appropriate transparency (alpha ~0.4)
- [ ] Edge line is visible to define the data boundary
- [ ] No overlapping axis labels or tick marks
- [ ] Colorblind-safe colors used
- [ ] Appropriate figure size (16x9 aspect ratio) for readability
- [ ] Title is centered and clearly readable if provided

## Expected Output

A clean area chart with a filled region between the data line and the x-axis baseline.
The fill should be semi-transparent to allow grid lines to show through while still emphasizing magnitude.
A solid edge line should clearly define the top boundary of the data.
The plot should be immediately understandable without additional explanation.
All text elements should be legible at standard display sizes.

## Tags

area, trend, time-series, basic, magnitude, cumulative, exploratory

## Use Cases

- Visualizing cumulative values over time (e.g., total revenue growth)
- Showing trends with emphasis on magnitude (e.g., stock prices)
- Comparing values to a baseline (e.g., temperature above/below average)
- Website traffic visualization over time
- Resource utilization monitoring (CPU, memory usage)
- Population or growth trends
