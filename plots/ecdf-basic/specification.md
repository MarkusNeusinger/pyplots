# ecdf-basic: Basic ECDF Plot

## Description

An ECDF (Empirical Cumulative Distribution Function) plot displays a step function that shows the proportion of observations less than or equal to each value. Unlike histograms, ECDF plots require no binning or smoothing, providing a non-parametric estimate of the cumulative distribution. The y-axis ranges from 0 to 1, allowing direct reading of percentiles and quantiles from the visualization.

## Applications

- Comparing distributions between groups to identify differences in spread, location, or shape
- Identifying distribution characteristics such as median, quartiles, and percentiles at a glance
- Statistical analysis and hypothesis testing where the full distribution shape matters
- Visualizing sample distributions without making parametric assumptions about the underlying data

## Data

- `values` (numeric) - Continuous variable to visualize
- Size: 50-500 observations (works well from 10 to 10000+ but 50-500 is ideal for visualization)
- Example: Random samples from a normal distribution

## Notes

- The step function should increase by 1/n at each data point
- Y-axis must range from 0 to 1 representing cumulative proportion
- Consider using a distinct line style for clarity
- Grid lines help with reading specific percentile values
