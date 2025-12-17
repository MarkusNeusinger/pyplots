# span-basic: Basic Span Plot (Highlighted Region)

## Description

A span plot highlights a specific region of interest on a chart using a shaded rectangular area that spans the full height or width of the plot. Vertical spans mark ranges along the x-axis (e.g., time periods), while horizontal spans mark ranges along the y-axis (e.g., value thresholds). The semi-transparent fill allows underlying data to remain visible while drawing attention to the highlighted region.

## Applications

- Marking recession periods or economic events on financial time series charts
- Highlighting acceptable/unacceptable value ranges or threshold zones on line plots
- Indicating maintenance windows, downtime periods, or significant events in operational dashboards
- Showing confidence intervals or uncertainty bands around data points

## Data

- `start` (numeric) - Start position of the span region
- `end` (numeric) - End position of the span region
- `direction` (categorical) - Either "vertical" (spans x-axis) or "horizontal" (spans y-axis)
- Size: 1-5 span regions overlaid on existing data
- Example: A line chart with dates on x-axis showing a shaded vertical span from 2008 to 2009 marking a recession period

## Notes

- Use semi-transparent fill (alpha 0.2-0.3) to keep underlying data visible
- Vertical spans are most common for time-based data (highlighting periods)
- Horizontal spans work well for threshold visualization (highlighting value ranges)
- Optional: include edge lines or text labels within the span region
