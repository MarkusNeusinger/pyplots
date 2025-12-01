# area-basic: Basic Area Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
-->

**Spec Version:** 1.0.0

## Description

Create a simple area chart that displays a single filled area beneath a line, ideal for showing how a quantity changes over time or another continuous variable. The filled area emphasizes the magnitude of values and cumulative totals.

## Data Requirements

- **x**: Numeric or datetime column for the x-axis (continuous variable, typically time or sequence)
- **y**: Numeric column for the y-axis (the values to plot)

## Optional Parameters

- `color`: Fill color for the area (type: string, default: "steelblue")
- `alpha`: Fill transparency level (type: float 0.0-1.0, default: 0.6)
- `line_color`: Color of the top line (type: string, default: same as color)
- `line_width`: Width of the top line (type: float, default: 1.5)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (16, 9))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3
- [ ] Area fill is clearly visible with appropriate transparency
- [ ] Line on top of area provides clear boundary
- [ ] No overlapping axis labels or tick marks
- [ ] Appropriate figure size (16:9 aspect ratio) for readability
- [ ] Title is centered and clearly readable if provided

## Expected Output

A clean area chart with a filled region showing values over a continuous axis. The area should be filled with a semi-transparent color, bounded by a line at the top edge. The baseline should be at y=0. Grid lines should help with reading values without overpowering the data. All text elements (labels, title, and tick labels) should be legible at standard display sizes.

## Tags

trend, time-series, basic, area, continuous, statistical, exploratory

## Use Cases

- Stock price or market value over time (e.g., portfolio value growth)
- Website traffic visualization (e.g., daily visitors over months)
- Resource usage monitoring (e.g., CPU or memory usage over time)
- Sales trends over time periods (e.g., monthly revenue)
- Temperature or environmental data over time
- Population growth or demographic changes
