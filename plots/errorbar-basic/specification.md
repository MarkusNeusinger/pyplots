# errorbar-basic: Basic Error Bar Plot

## Description

An error bar plot displays data points with associated uncertainty or variability represented by bars extending above and below (or left and right of) each point. Error bars commonly represent standard deviation, standard error, confidence intervals, or min/max ranges. This visualization is essential for communicating the reliability and precision of measurements or statistical estimates.

## Applications

- Scientific research presenting experimental results with measurement uncertainty
- Statistical analysis comparing group means with confidence intervals
- Quality control monitoring showing acceptable tolerance ranges around targets
- Clinical trials displaying treatment effects with error margins

## Data

- `x` (categorical or numeric) - Categories or positions on the x-axis
- `y` (numeric) - Central values representing mean, median, or measured values
- `error` (numeric) - Error magnitude for symmetric error bars, or tuple/pair for asymmetric errors
- Size: 3-20 groups/points for clarity

## Notes

- Error bars should have visible caps (horizontal lines at ends) to clearly mark the error range
- Use consistent error bar widths across all data points
- Consider using different colors to distinguish between groups when comparing multiple series
- Asymmetric error bars may be needed for skewed distributions or log-transformed data
