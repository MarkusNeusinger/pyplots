# timeseries-decomposition: Time Series Decomposition Plot

## Description

A time series decomposition plot displays a time series broken down into its constituent components: the original series, trend, seasonal pattern, and residual noise. Each component is shown as a separate subplot stacked vertically, sharing a common time axis. This visualization is essential for understanding the underlying structure of time series data and identifying patterns that may not be visible in the raw series.

## Applications

- Analyzing sales data to separate long-term growth trends from seasonal holiday patterns
- Decomposing temperature records to isolate climate trends from annual cycles
- Understanding stock market behavior by separating systematic patterns from random fluctuations
- Preprocessing time series for forecasting by examining component predictability

## Data

- `date` (datetime) - Sequential timestamps at regular intervals (daily, monthly, etc.)
- `value` (numeric) - Continuous measurements or observations at each timestamp
- Size: 100-1000 points (minimum 2 full seasonal cycles for meaningful decomposition)
- Example: Monthly airline passengers over 10 years, daily retail sales over 2 years

## Notes

- Display four vertically stacked subplots: Original, Trend, Seasonal, and Residual
- Use consistent x-axis (time) across all subplots for easy comparison
- Label each subplot clearly with component name
- Consider using statsmodels seasonal_decompose or similar for decomposition
- Additive decomposition is typical; multiplicative may be needed for data with proportional seasonality
- Include light grid lines to aid reading values across time
