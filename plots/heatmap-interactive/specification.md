# heatmap-interactive: Interactive Heatmap with Hover and Zoom

## Description

An interactive heatmap with hover tooltips that display cell values and zoom/pan capabilities for exploring large matrices. Essential for datasets too large to display all values at once, allowing users to drill down into specific regions while maintaining context. The interactive features enable efficient exploration of patterns, correlations, and outliers in complex matrix data.

## Applications

- Exploring large correlation matrices in financial or scientific research
- Interactive gene expression analysis in bioinformatics dashboards
- Real-time performance monitoring matrices with drill-down capability
- User behavior analysis on large website interaction matrices

## Data

- `x` (string/numeric) - column labels for the matrix
- `y` (string/numeric) - row labels for the matrix
- `value` (numeric) - cell values for color mapping and tooltip display
- Size: 10-100 rows, 10-100 columns (optimized for interactive exploration)

## Notes

- Hover tooltips must show row label, column label, and exact value
- Zoom/pan should be smooth and maintain cell visibility
- Include reset button or double-click to reset view
- Colorbar legend should update or remain visible during zoom
- Consider crosshair or highlight effect on hover for large matrices
