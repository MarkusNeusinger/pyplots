# scatter-regression-polynomial: Scatter Plot with Polynomial Regression

## Description

A scatter plot displaying the relationship between two numeric variables with a fitted polynomial regression curve (degree 2-4). This visualization extends beyond linear regression to capture non-linear relationships in data, making it ideal for modeling curved trends, parabolic patterns, and complex data relationships where a straight line would not adequately represent the underlying pattern.

## Applications

- Analyzing diminishing returns in economics where initial gains decrease over time
- Studying growth curves in biology where populations follow sigmoid or exponential patterns
- Modeling physical phenomena like projectile motion or thermal expansion with quadratic relationships

## Data

- `x` (numeric) - Independent variable values plotted on the horizontal axis
- `y` (numeric) - Dependent variable values plotted on the vertical axis following a non-linear relationship
- Size: 30-300 points recommended for clear polynomial curve visualization
- Example: Data with a clear curved pattern such as quadratic, cubic, or sigmoid trends

## Notes

- Display R² value prominently on the plot to indicate goodness of fit
- Polynomial curve should be visually distinct from scatter points (solid line, contrasting color)
- Use polynomial degree 2 (quadratic) as default; higher degrees (3-4) for more complex curves
- Optional: Include confidence band with semi-transparent shading around the fitted curve
- Points should have moderate transparency (alpha ~0.6-0.7) to show density
- Include axis labels and descriptive title mentioning polynomial regression
- Consider annotating with the polynomial equation (y = ax² + bx + c)
- Avoid overfitting: higher-degree polynomials should only be used when justified by data pattern
