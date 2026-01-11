# area-stock-range: Stock Area Chart with Range Selector

## Description

A filled area chart specifically designed for stock price visualization, showing price history with the area below the price line filled to emphasize price movements and trends. The distinguishing feature is an interactive range selector that allows users to zoom into specific time periods, making it ideal for exploring price patterns across different time scales. Common in financial dashboards where users need to analyze both long-term trends and short-term price action.

## Applications

- Visualizing stock price history in trading platforms and financial dashboards
- Analyzing cryptocurrency price trends with the ability to zoom into specific periods
- Portfolio value tracking over time with interactive time range exploration
- Comparing asset performance across different market conditions by selecting relevant date ranges

## Data

- `date` (datetime) - Trading dates or timestamps for price observations
- `price` (numeric) - Closing price or adjusted price values
- Size: 100-1000+ data points for meaningful range selection
- Example: Daily closing prices for a stock over 2-5 years with range selector spanning the full history

## Notes

- Range selector should allow both preset ranges (1M, 3M, 6M, 1Y, YTD, All) and custom date selection
- Use a mini chart in the range selector to provide context of the full data range
- Fill color should be semi-transparent (alpha 0.3-0.5) with a solid line on top
- Consider using gradient fill from bottom to emphasize price levels
- Main chart should update smoothly when range selection changes
- Include clear date formatting on x-axis that adapts to the selected range
