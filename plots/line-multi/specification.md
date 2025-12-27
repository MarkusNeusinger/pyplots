# line-multi: Multi-Line Comparison Plot

## Description

A multi-line plot displays multiple data series on the same axes for direct comparison. Each series is represented by a distinct line with its own color and optional style, making it easy to identify trends, correlations, and divergences between variables. This visualization is essential for comparing related metrics over a common sequence or time period.

## Applications

- Comparing stock prices or financial metrics of multiple companies over trading days
- Tracking performance metrics of different products or campaigns over time
- Analyzing temperature or weather patterns across multiple cities or regions

## Data

- `x` (numeric/datetime) - Shared sequential or time values for alignment
- `y1, y2, ...` (numeric) - Multiple continuous series to compare
- `series` (categorical) - Optional grouping variable if data is in long format
- Size: 10-200 points per series, 2-6 series recommended
- Example: Monthly sales for 3 product lines, daily stock prices for 4 companies

## Notes

- Use distinct colors for each line to ensure clear differentiation
- Include a legend that clearly identifies each series
- Consider varying line styles (solid, dashed, dotted) for additional distinction
- Optional markers at data points can improve readability for sparse data
- Keep the number of series manageable (2-6) to avoid visual clutter
