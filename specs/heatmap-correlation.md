# heatmap-correlation: Correlation Matrix Heatmap

<!--
Spec Template Version: 1.0.0
Last Updated: 2025-01-24
-->

**Spec Version:** 1.0.0

## Description

Create a heatmap visualization of the correlation matrix for numerical columns in a dataset. This plot shows the Pearson correlation coefficients between all pairs of numeric variables, helping identify relationships and dependencies between features in multivariate data.

## Data Requirements

- **data**: A DataFrame containing at least 2 numeric columns for correlation calculation

## Optional Parameters

- `figsize`: Figure size in inches (type: tuple, default: (10, 8))
- `cmap`: Color map for the heatmap (type: str, default: 'coolwarm' or library default)
- `annot`: Show correlation values in cells (type: bool, default: True)
- `fmt`: Format string for annotations (type: str, default: '.2f')
- `mask_upper`: Mask the upper triangle for cleaner display (type: bool, default: False)
- `vmin`: Minimum value for color scale (type: float, default: -1.0)
- `vmax`: Maximum value for color scale (type: float, default: 1.0)
- `title`: Plot title (type: str, default: 'Correlation Matrix')

## Quality Criteria

- [ ] Heatmap displays correlation values for all numeric column pairs
- [ ] Color scale clearly differentiates positive (warm) and negative (cool) correlations
- [ ] Correlation values are displayed in each cell with 2 decimal precision
- [ ] Column and row labels are readable and not overlapping
- [ ] Color bar shows the correlation scale from -1 to 1
- [ ] Figure has appropriate aspect ratio (square or near-square for correlation matrix)
- [ ] Diagonal values show perfect correlation (1.0) for self-correlation

## Expected Output

The plot should display a square or rectangular heatmap where each cell represents the Pearson correlation coefficient between two variables. The color intensity should represent the strength of correlation, typically using a diverging color scheme where red/warm colors indicate positive correlation, blue/cool colors indicate negative correlation, and white/neutral indicates no correlation. The actual correlation values should be displayed in each cell for easy reading. The axes should show all variable names clearly, and a color bar should provide reference for the correlation scale.

## Tags

heatmap, correlation, statistical, multivariate

## Use Cases

- Feature selection in machine learning to identify correlated predictors
- Exploratory data analysis in financial datasets to find asset correlations
- Quality control in manufacturing to identify related process parameters
- Medical research to find relationships between clinical measurements
- Market research to understand customer behavior patterns across variables
- Climate data analysis to identify relationships between weather variables