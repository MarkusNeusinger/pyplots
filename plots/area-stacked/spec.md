# area-stacked: Stacked Area Chart

## Description

A stacked area chart displaying multiple data series as filled layers stacked on top of each other. Each layer represents a component of the total, with the cumulative height showing the aggregate value at any point. This visualization excels at showing both individual contributions and total magnitude over time, making part-to-whole relationships immediately visible.

## Applications

- Comparing market share of competing products over time
- Visualizing revenue breakdown by product category across quarters
- Tracking energy consumption by source (solar, wind, fossil) over years
- Showing traffic distribution across different channels or sources

## Data

- `x` (datetime) - time-based sequential values for the horizontal axis
- `y1`, `y2`, `y3`, `y4` (numeric) - values for each stacked layer
- Size: 12-50 time points, 3-4 data series
- Example: monthly revenue by product line over 2 years

## Notes

- Use semi-transparent fills (alpha 0.7-0.8) for visual depth
- Choose a sequential or qualitative color palette with good contrast
- Include a clear legend to identify each layer
- Add subtle grid lines for readability
- Consider ordering layers by magnitude (largest at bottom) for stability
