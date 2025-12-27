# bar-error: Bar Chart with Error Bars

## Description

A bar chart with error bars displays categorical data as rectangular bars with vertical (or horizontal) lines extending from each bar to indicate uncertainty or variability. Error bars typically represent standard deviation, standard error, confidence intervals, or min/max ranges. This visualization is essential for comparing group means while communicating the reliability and precision of each measurement.

## Applications

- Scientific experiments comparing treatment groups with measurement uncertainty
- Survey results displaying response means with confidence intervals
- A/B test results showing conversion rates with statistical bounds
- Comparing group means with standard deviations across categories

## Data

- `category` (categorical) - Names or labels for each bar
- `value` (numeric) - Central value for each bar (mean, median, or measured value)
- `error` (numeric) - Error magnitude for symmetric error bars, or pair for asymmetric errors (lower, upper)
- Size: 3-12 categories for optimal readability

## Notes

- Error bars should have visible caps (horizontal lines at ends) to clearly mark the error range
- Include a legend or annotation explaining what the error bars represent (e.g., "±1 SD", "95% CI")
- Consider horizontal orientation when category labels are long or numerous
- Use consistent bar widths and error bar styling across all categories
- Asymmetric error bars may be needed for skewed distributions or percentage data
