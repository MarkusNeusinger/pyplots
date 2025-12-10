# heatmap-correlation: Correlation Matrix Heatmap

## Description

A correlation heatmap visualizes the pairwise correlation coefficients between multiple numeric variables in a matrix format. Each cell is color-coded to represent the strength and direction of correlation, with values ranging from -1 (perfect negative correlation) to +1 (perfect positive correlation). This plot is essential for exploratory data analysis to identify relationships between variables quickly.

## Applications

- Analyzing feature correlations in machine learning datasets to identify multicollinearity before model training
- Financial portfolio analysis to understand how different asset returns move together
- Survey response analysis to discover which questions or metrics are related

## Data

- `variables` (list of strings) - Names of the variables being correlated
- `correlation_matrix` (2D numeric array) - Square matrix of correlation coefficients (-1 to 1)
- Size: 5-20 variables (larger matrices become difficult to read)
- Example: Correlation matrix computed from numeric columns of a dataset using pandas `df.corr()`

## Notes

- Use a diverging color palette (e.g., blue for negative, white for zero, red for positive correlations)
- Display correlation values as text annotations in each cell for precise reading
- Consider masking the upper or lower triangle since the matrix is symmetric
- Diagonal always contains 1.0 (self-correlation) and can be highlighted or masked
