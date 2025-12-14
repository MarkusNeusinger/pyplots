# heatmap-basic: Basic Heatmap

## Description

A heatmap displaying values in a matrix format using color intensity. Each cell's color represents the magnitude of the value, making it easy to identify patterns, clusters, and outliers in two-dimensional data. Essential for visualizing correlations, frequencies, and relationships between variables.

## Applications

- Correlation matrices between variables in statistical analysis
- Website click heatmaps showing user behavior patterns
- Gene expression analysis in bioinformatics research
- Performance metrics across time periods and categories

## Data

- `x` (string/numeric) - column labels for the matrix
- `y` (string/numeric) - row labels for the matrix
- `value` (numeric) - cell values for color mapping
- Size: 5-50 rows, 5-50 columns

## Notes

- Use a diverging colormap for data with positive/negative values
- Add value annotations in cells when readable
- Include a colorbar legend
- Consider clustering rows/columns for better pattern visibility
