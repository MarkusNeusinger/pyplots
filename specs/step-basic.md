# step-basic: Basic Step Plot

<!--
Spec Template Version: 1.0.0
Created: 2025-11-28
Last Updated: 2025-11-28
-->

**Spec Version:** 1.0.0

## Description

Create a basic step plot showing discrete changes in values over sequential points or time.
Step plots display data as a series of horizontal and vertical lines, showing discrete changes between values.
Ideal for visualizing data that changes at specific intervals, such as interest rates, inventory levels, or staged processes.

## Data Requirements

- **x**: Sequential or time-based values (numeric or datetime: ordered values)
- **y**: Numeric values representing the levels at each step (numeric: continuous values)

## Optional Parameters

- `where`: Position of steps (type: string, default: "pre", options: "pre", "post", "mid")
- `color`: Line color (type: string, default: "steelblue")
- `linewidth`: Line width (type: float, default: 2.0)
- `alpha`: Transparency level (type: float 0.0-1.0, default: 0.9)
- `linestyle`: Line style (type: string, default: "-", options: "-", "--", "-.", ":")
- `marker`: Marker style for data points (type: string, default: None, e.g., "o", "s", "^")
- `markersize`: Size of markers if used (type: float, default: 6)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (10, 6))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle (alpha=0.3) on both axes
- [ ] Step lines are clearly visible with appropriate width (linewidth ≥ 2)
- [ ] No overlapping axis labels or tick marks
- [ ] Steps are correctly positioned according to 'where' parameter
- [ ] Data points accurately represent the discrete changes
- [ ] Appropriate figure size (10x6 inches default) for readability
- [ ] Title is centered and clearly readable if provided (fontsize 14, bold)

## Expected Output

A clean step plot showing discrete changes between data points with horizontal and vertical lines.
The plot should clearly show when and how values change, with horizontal lines representing periods of constant value and vertical lines showing the transitions.
The 'where' parameter should control whether the step occurs before the data point ("pre"), after ("post"), or at the midpoint ("mid").
Grid lines should help with reading values without overpowering the data.
If markers are specified, they should appear at the actual data points to help distinguish the measurement positions.
All text elements should be legible at standard display sizes.

## Tags

line, step, timeseries, basic, trend, sequential, discrete

## Use Cases

- Interest rate changes over time (e.g., central bank rate adjustments)
- Inventory levels in supply chain management (e.g., stock levels after each order)
- Digital signal processing (e.g., sampled analog-to-digital conversion)
- Pricing tiers or rate schedules (e.g., progressive tax brackets)
- Manufacturing process stages (e.g., temperature settings in batch processing)
- Resource allocation over project phases (e.g., staffing levels per sprint)