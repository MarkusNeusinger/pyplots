# residual-plot: Residual Plot

## Description

A residual plot displays the difference between observed and predicted values (residuals) against fitted values or an independent variable in regression analysis. This diagnostic visualization helps identify violations of regression assumptions including non-linearity, heteroscedasticity (non-constant variance), and outliers. A well-fitting model shows residuals randomly scattered around zero with no discernible pattern.

## Applications

- Validating linear regression model assumptions by checking for random residual distribution
- Detecting non-linear relationships that suggest the need for polynomial or transformed features
- Identifying heteroscedasticity where prediction errors vary with fitted values
- Locating influential outliers and leverage points that may distort model coefficients
- Comparing model fit quality across different regression specifications

## Data

- `y_true` (numeric array) - Observed/actual target values
- `y_pred` (numeric array) - Predicted values from regression model
- Residuals calculated as: `residuals = y_true - y_pred`
- Size: 50-1000 observations typical for regression diagnostics
- Example: Linear regression predictions from sklearn with residuals

## Notes

- Include a horizontal reference line at y=0 representing perfect predictions
- Plot residuals on y-axis against fitted values on x-axis (standard residual plot)
- Use alpha transparency for overlapping points when sample size is large
- Optional: Add LOWESS or kernel smoothing line to detect non-linear patterns in residuals
- Consider adding horizontal bands at ±2 standard deviations to identify potential outliers
- Color outliers differently if residuals exceed threshold (e.g., 2 or 3 standard deviations)
