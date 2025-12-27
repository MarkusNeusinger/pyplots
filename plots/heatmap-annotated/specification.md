# heatmap-annotated: Annotated Heatmap

## Description

A heatmap with numeric values displayed inside each cell, combining color intensity with exact value labels. Essential for correlation matrices, confusion matrices, and any matrix visualization where both pattern recognition and precise values matter. Text color automatically contrasts with background for readability.

## Applications

- Correlation matrices showing relationships between variables with exact coefficients
- Confusion matrices in machine learning model evaluation
- Performance matrices comparing metrics across categories and time periods
- Statistical analysis requiring both visual patterns and precise values

## Data

- `x` (string/numeric) - column labels for the matrix
- `y` (string/numeric) - row labels for the matrix
- `value` (numeric) - cell values for color mapping and annotation
- Size: 5-20 rows, 5-20 columns (larger matrices may have readability issues)

## Notes

- Text annotations must have sufficient contrast with background color
- Use appropriate number formatting (e.g., 2 decimal places for correlations)
- Include a colorbar legend showing the value scale
- Consider font size relative to cell size for readability
- Diverging colormap recommended for data with positive/negative values
