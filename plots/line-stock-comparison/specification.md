# line-stock-comparison: Stock Price Comparison Chart

## Description

A multi-line chart comparing multiple stock price series normalized to a common starting point (rebased to 100) for direct performance comparison over time. By rebasing all series to the same initial value, investors can easily compare relative returns regardless of absolute price differences. This visualization reveals which stocks outperformed or underperformed relative to each other, making it essential for portfolio analysis and benchmark comparisons.

## Applications

- Comparing performance of multiple stocks in an investment portfolio
- Benchmark comparison (individual stock vs S&P 500 or sector index)
- Sector comparison analysis across competing companies
- Investment strategy backtesting visualization

## Data

- `date` (datetime) - Trading dates for price observations
- `symbol` (string) - Stock ticker symbol (e.g., AAPL, GOOGL)
- `price` (numeric) - Adjusted closing price
- Size: 200-300 points per series (approximately 1 year of daily data), 2-10 series
- Example: Daily closing prices for AAPL, GOOGL, MSFT, and SPY over one year

## Notes

- Normalize all series to 100 at the first date (rebased = price / first_price * 100)
- Use distinct colors for each stock with a clear legend identifying symbols
- Y-axis should show rebased values (percentage change from start, centered around 100)
- Consider adding a horizontal reference line at 100 to indicate the starting point
- Optional: highlight specific events or time periods with vertical spans or annotations
- Grid lines improve readability for tracking relative performance
