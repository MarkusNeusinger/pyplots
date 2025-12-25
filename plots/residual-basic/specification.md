# residual-basic: Residual Plot

## Description

A residual plot displays residuals (differences between observed and predicted values) against fitted values from a regression model. This diagnostic visualization is essential for validating regression assumptions, identifying patterns in model errors, checking for heteroscedasticity (non-constant variance), and detecting outliers or influential observations that may affect model reliability.

## Applications

- Validating linear regression assumptions in statistical modeling by checking for random scatter of residuals
- Identifying heteroscedasticity in econometric models to determine if weighted least squares is needed
- Detecting outliers and influential observations in predictive modeling that may require investigation or removal

## Data

- `fitted` (numeric) - Predicted values from the regression model, plotted on the horizontal axis
- `residuals` (numeric) - Differences between observed and predicted values (y - y_hat), plotted on the vertical axis
- Size: 30-500 points recommended for clear pattern detection
- Example: Residuals from a linear regression model showing ideally random scatter around zero

## Notes

- Include a horizontal reference line at y=0 to help assess systematic bias
- Points should have moderate transparency (alpha ~0.6) to reveal density and overlapping observations
- Consider adding a smoothed trend line (LOWESS/LOESS) to detect non-linear patterns in residuals
- Axis labels should clearly indicate "Fitted Values" and "Residuals"
- Title should reference the diagnostic purpose (e.g., "Residual Plot for Regression Diagnostics")
- Symmetric y-axis range around zero is preferred for visual balance
