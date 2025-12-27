# heatmap-correlation: Correlation Matrix Heatmap

## Description

A heatmap specifically designed to display correlation coefficients between variables, using a diverging color scheme centered at zero. The symmetric matrix visualization makes it easy to identify positive correlations, negative correlations, and independent variables at a glance. Essential for exploratory data analysis, feature engineering, and multicollinearity detection in statistical and machine learning workflows.

## Applications

- Feature correlation analysis in machine learning to identify redundant predictors
- Understanding variable relationships in exploratory data analysis
- Multicollinearity detection before regression modeling
- Portfolio diversification analysis in finance

## Data

- `variables` (string) - variable names for both axes
- `correlation_matrix` (numeric) - square matrix of correlation values ranging from -1 to 1
- Size: 5-15 variables (larger matrices may have readability issues)

## Notes

- Use a diverging colormap (e.g., blue-white-red or coolwarm) centered at zero
- Annotate cells with correlation values (2 decimal places)
- Display as symmetric matrix with variable names on both axes
- Consider masking upper or lower triangle to reduce redundancy
- Set colorbar range to fixed -1 to 1 for consistent interpretation
