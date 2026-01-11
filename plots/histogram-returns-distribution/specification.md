# histogram-returns-distribution: Returns Distribution Histogram

## Description

A histogram showing the distribution of financial returns (daily, weekly, or monthly) with a normal distribution overlay for comparison. This visualization is essential for risk analysis, allowing analysts to assess whether returns follow a normal distribution, identify fat tails indicating higher-than-expected extreme events, and measure asymmetry through skewness. Key statistics are displayed directly on the plot for quick interpretation.

## Applications

- Risk analysis and return distribution assessment for portfolio management
- Comparing actual return distributions to theoretical normal distribution assumptions
- Identifying fat tails and skewness in financial time series for VaR calculations
- Evaluating portfolio return characteristics and risk metrics

## Data

- `date` (datetime) - Period dates for the returns
- `returns` (numeric) - Percentage returns (daily, weekly, or monthly)
- Size: 252+ observations recommended (1 year of daily data)
- Example: Daily stock returns, ETF returns, or portfolio returns

## Notes

- Show percentage returns on x-axis with clear labels
- Overlay normal distribution curve fitted to the data for comparison
- Display key statistics in a text box: mean, standard deviation, skewness, kurtosis
- Highlight tail regions beyond 2 standard deviations with distinct coloring
- Use appropriate bin width for return data (typically 20-50 bins for 252+ observations)
- Consider using density normalization so histogram and normal curve are on comparable scales
