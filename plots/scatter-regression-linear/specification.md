# scatter-regression-linear: Scatter Plot with Linear Regression

## Description

A scatter plot that displays the relationship between two numeric variables with a fitted linear regression line and confidence interval band. This visualization extends the basic scatter plot by adding statistical modeling elements, making it ideal for understanding linear relationships, assessing model fit, and communicating the strength of correlations with visual uncertainty quantification.

## Applications

- Analyzing the relationship between advertising spend and sales revenue with prediction confidence
- Studying the correlation between study hours and exam scores in educational research
- Investigating the linear relationship between temperature and energy consumption in utility planning

## Data

- `x` (numeric) - Independent variable values plotted on the horizontal axis
- `y` (numeric) - Dependent variable values plotted on the vertical axis
- Size: 30-300 points recommended for clear regression visualization
- Example: Correlated data with noise to demonstrate regression fit and confidence intervals

## Notes

- Display R² or correlation coefficient (r) prominently on the plot
- Regression line should be visually distinct from scatter points (solid line, contrasting color)
- Confidence band should use semi-transparent shading (95% CI recommended)
- Points should have moderate transparency (alpha ~0.6-0.7) to show density
- Include axis labels and descriptive title mentioning the regression analysis
- Consider adding the regression equation (y = mx + b) as annotation
