# scatter-matrix: Scatter Plot Matrix

## Description

A grid of scatter plots showing all pairwise relationships between multiple variables, with histograms or kernel density estimates on the diagonal. This comprehensive visualization enables simultaneous exploration of correlations and distributions across an entire dataset, making it invaluable for understanding multivariate data structure at a glance. Also known as a pairplot or SPLOM (Scatter Plot Matrix).

## Applications

- Exploratory data analysis to quickly identify correlations, clusters, and outliers across multiple features in a dataset
- Feature selection in machine learning by visually assessing variable relationships before modeling
- Dataset overview and quality checking to understand distributions and detect anomalies in multivariate data

## Data

- `variables` (list of numeric columns) - Multiple continuous variables to compare pairwise
- Variables: 3-6 recommended for clarity (grid grows quadratically)
- Size: 50-500 points recommended per scatter for visual clarity
- Example: Iris dataset or similar multivariate numeric data

## Notes

- Diagonal cells should show univariate distributions (histograms or KDE) for each variable
- Off-diagonal cells show scatter plots for each variable pair
- Variable names should appear along the edges (left and bottom) as axis labels
- Consider using color encoding to show categorical groupings if available
- Keep point size small and use transparency to handle overplotting in dense datasets
- Matrix should be symmetric (upper and lower triangles show same relationships)
