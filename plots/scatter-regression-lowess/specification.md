# scatter-regression-lowess: Scatter Plot with LOWESS Regression

## Description

A scatter plot with a LOWESS (Locally Weighted Scatterplot Smoothing) regression curve overlaid. LOWESS is a non-parametric method that fits smooth curves by performing local weighted regressions at each point, adapting to local data patterns without assuming a specific functional form. This makes it ideal for exploring complex relationships where the underlying pattern is unknown or varies across the data range.

## Applications

- Exploring non-linear relationships in exploratory data analysis where the true relationship is unknown
- Visualizing trends in economic data where patterns may change over different value ranges
- Analyzing biological dose-response curves that don't follow standard mathematical models

## Data

- `x` (numeric) - Independent variable values plotted on the horizontal axis
- `y` (numeric) - Dependent variable values plotted on the vertical axis
- Size: 50-500 points recommended (LOWESS benefits from moderate sample sizes)
- Example: Data with a complex, non-linear relationship that varies across the x-axis range

## Notes

- LOWESS curve should be visually distinct from scatter points (solid line, contrasting color)
- Use moderate smoothing bandwidth (frac ~0.3-0.5) as default for balanced smoothness
- Points should have moderate transparency (alpha ~0.5-0.7) to show density and the fitted curve clearly
- Include axis labels and descriptive title mentioning LOWESS smoothing
- Optional: Show confidence band around the LOWESS curve if library supports it
- The curve should appear smooth without excessive oscillation or overfitting to noise
