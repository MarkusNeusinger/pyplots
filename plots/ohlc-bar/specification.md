# ohlc-bar: OHLC Bar Chart

## Description

An OHLC (Open-High-Low-Close) bar chart displays financial price data using vertical bars with horizontal tick marks. Each bar shows the price range from high to low as a thin vertical line, with a left tick indicating the opening price and a right tick indicating the closing price. Unlike candlestick charts that use colored bodies, OHLC bars provide a cleaner, less cluttered view favored by technical analysts who prefer to focus on price levels rather than visual patterns.

## Applications

- Analyzing daily stock price movements with focus on precise price levels
- Comparing price action across multiple securities on the same chart without color distraction
- Technical analysis where traders prefer bar charts over candlesticks for pattern recognition

## Data

- `date` (datetime) - The time period for each bar (e.g., day, hour, minute)
- `open` (numeric) - Opening price at the start of the period
- `high` (numeric) - Highest price during the period
- `low` (numeric) - Lowest price during the period
- `close` (numeric) - Closing price at the end of the period
- Size: 20-100 periods for clear visualization
- Example: Daily OHLC prices for a stock over 30-60 trading days

## Notes

- Use thin vertical lines for the high-low range
- Horizontal ticks should extend to the left for open and right for close
- Consider using different colors for up bars (close > open) vs down bars (close < open) for easier reading
- Time axis should have appropriate date formatting based on data frequency
- Grid lines help read exact price levels
