# area-basic: Basic Area Chart

## Description

An area chart showing quantitative data over a continuous axis with the area below the line filled. It emphasizes the magnitude of values over time by filling the space between the line and axis, creating visual weight that helps readers understand volume and trends. Particularly effective for showing cumulative totals, resource consumption, or any data where the "amount" is as important as the trend.

## Applications

- Website traffic over time showing visitor volume
- Revenue trends with cumulative effect visualization
- Stock price movements with volume emphasis
- Resource utilization (CPU, memory) over time

## Data

- `x` (datetime/numeric) - continuous axis values, typically time
- `y` (numeric) - values to plot representing magnitude
- Size: 20-500 data points
- Example: daily website visitors over a month

## Notes

- Use semi-transparent fill (alpha 0.3-0.5) for better readability
- Include gridlines for value estimation
- Add clear axis labels with units
- Consider gradient fill from bottom to line for visual appeal
