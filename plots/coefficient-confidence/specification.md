# coefficient-confidence: Coefficient Plot with Confidence Intervals

## Description

A coefficient plot displays regression coefficients as points positioned along a horizontal axis, with horizontal error bars showing confidence intervals. This visualization makes it easy to assess effect sizes and statistical significance - coefficients whose confidence intervals cross zero are not statistically significant. Typically used to summarize results from linear, logistic, or other regression models in a clear, publication-ready format.

## Applications

- Visualizing effect sizes and significance from multiple regression models
- Comparing predictor importance in linear or logistic regression analysis
- Presenting regression results in academic publications and reports
- Communicating which variables have significant effects in statistical models

## Data

- `variable` (str) - Name of the predictor variable or coefficient
- `coefficient` (float) - Point estimate of the regression coefficient
- `ci_lower` (float) - Lower bound of the confidence interval
- `ci_upper` (float) - Upper bound of the confidence interval
- `significant` (bool, optional) - Whether the coefficient is statistically significant
- Size: 5-20 coefficients for optimal readability
- Example: Coefficients from a multiple linear regression predicting housing prices

## Notes

- Vertical reference line at zero to indicate the null hypothesis threshold
- Variables typically ordered by coefficient magnitude for easier comparison
- Use different colors or markers to distinguish significant vs non-significant coefficients
- Horizontal layout (coefficients on y-axis, values on x-axis) preferred for readability with long variable names
- Include axis label indicating the effect measure (e.g., "Coefficient Estimate", "Log Odds Ratio")
