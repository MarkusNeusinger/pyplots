# candlestick-basic: Basic Candlestick Chart

## Description

A candlestick chart displays open, high, low, and close (OHLC) price data for financial instruments over time. Each candlestick shows the price range within a specific period, with the body indicating the open-close range and the wicks (shadows) showing the high-low range. Color coding distinguishes bullish (price increase) from bearish (price decrease) periods, making it easy to identify trends and price patterns at a glance.

## Applications

- Tracking daily stock price movements to identify trends and potential entry/exit points
- Analyzing cryptocurrency volatility and price action over hourly or daily intervals
- Visualizing forex currency pair movements for technical analysis

## Data

- `date` (datetime) - The time period for each candlestick (e.g., day, hour)
- `open` (numeric) - Opening price at the start of the period
- `high` (numeric) - Highest price during the period
- `low` (numeric) - Lowest price during the period
- `close` (numeric) - Closing price at the end of the period
- Size: 20-100 periods for clear visualization
- Example: Daily OHLC prices for a stock over 30 trading days

## Notes

- Use green/red or blue/red color schemes for up/down days (green/red is most common)
- Ensure wicks are clearly visible but thinner than the candle body
- Time axis should have appropriate date formatting based on the data frequency
- Consider adding a subtle grid to help read price levels
