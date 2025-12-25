# area-stacked: Stacked Area Chart

## Description

A stacked area chart displays multiple data series as areas stacked on top of each other, with each series starting where the previous one ends. This visualization emphasizes both individual contributions and cumulative totals over a continuous axis (typically time). It is ideal for showing how parts contribute to a whole while tracking changes over time, making patterns of composition and overall trends immediately visible.

## Applications

- Revenue breakdown by product line over time
- Website traffic sources (direct, organic, referral, social) over months
- Resource allocation across departments or projects
- Energy consumption by sector over years

## Data

- `x` (datetime/numeric) - continuous axis values, typically time periods
- `y1, y2, y3, ...` (numeric) - values for each series to be stacked
- `category` (categorical) - labels identifying each series
- Size: 10-100 time points, 2-8 series
- Example: monthly revenue by product category over two years

## Notes

- Use distinct but harmonious colors for each series
- Order series by size (largest at bottom) for easier reading
- Include legend to identify each series
- Consider using semi-transparent fills for overlapping visibility
- Ensure baseline starts at zero to avoid misleading proportions
