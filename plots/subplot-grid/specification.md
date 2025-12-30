# subplot-grid: Subplot Grid Layout

## Description

A customizable grid of multiple subplots allowing different plot types in each cell, with shared or independent axes. Unlike faceted plots that repeat the same visualization for data subsets, subplot grids enable combining distinct visualizations (scatter, line, bar, histogram, etc.) into a cohesive multi-panel figure for comprehensive data presentation.

## Applications

- Dashboard-style visualizations combining multiple metrics in a single figure
- Scientific publications requiring related but distinct plots side-by-side
- Exploratory data analysis comparing different visualization approaches
- Technical reports showing complementary views of the same dataset

## Data

- `x` (numeric or categorical) - Primary variable for each subplot
- `y` (numeric) - Secondary variable for each subplot
- Size: Varies per subplot, typically 20-200 points per cell
- Example: Financial dashboard with price line chart, volume bars, and returns histogram

## Notes

- Grid dimensions should be configurable (e.g., 2x2, 2x3, 3x1)
- Support both shared axes (for comparison) and independent axes (for different scales)
- Each cell can contain a different plot type
- Consistent spacing and alignment across all subplots
- Clear titles or labels for each subplot to identify its content
