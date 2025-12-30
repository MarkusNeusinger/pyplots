# errorbar-asymmetric: Asymmetric Error Bars Plot

## Description

An asymmetric error bar plot displays data points with separate upper and lower error magnitudes, allowing different-sized bars extending above and below each point. This visualization is essential for representing skewed distributions, non-symmetric confidence intervals, or data where uncertainty differs in positive and negative directions. Common applications include percentile-based intervals, log-transformed data, and Bayesian credible intervals.

## Applications

- Scientific research presenting results with non-symmetric confidence intervals (e.g., 5th-95th percentile)
- Financial forecasting showing different upside and downside risk projections
- Clinical trials displaying treatment effects with asymmetric uncertainty bounds
- Environmental monitoring reporting measurements with different detection limits above and below

## Data

- `x` (categorical or numeric) - Categories or positions on the x-axis
- `y` (numeric) - Central values representing mean, median, or point estimates
- `error_lower` (numeric) - Error magnitude extending below each point
- `error_upper` (numeric) - Error magnitude extending above each point
- Size: 3-20 data points for clarity

## Notes

- Error bars should have visible caps (horizontal lines at ends) to clearly mark the error range
- Consider using different colors or markers when comparing multiple series
- Include a legend or annotation explaining what the asymmetric bounds represent (e.g., "10th-90th percentile", "95% CI")
- Useful for log-scale axes where symmetric intervals would appear asymmetric after transformation
