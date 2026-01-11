# drawdown-basic: Drawdown Chart

## Description

A drawdown chart visualizes the percentage decline from peak value over time, showing how far an investment or asset has fallen from its highest point. This chart is essential for risk assessment and understanding the magnitude of losses during unfavorable market periods. The filled area below the zero line emphasizes the depth and duration of drawdowns, making it easy to identify maximum drawdown periods and recovery points.

## Applications

- Risk management analysis to identify maximum drawdown periods and evaluate worst-case scenarios
- Portfolio performance evaluation comparing drawdown characteristics across different assets or strategies
- Investment decision-making by visualizing historical recovery times and drawdown frequencies
- Trading strategy assessment to understand downside risk and volatility patterns

## Data

- `date` (datetime) - Trading dates or time periods
- `price` or `value` (numeric) - Asset price, portfolio value, or cumulative returns
- Size: 250-1500 data points (1-5 years of daily data)
- Example: Daily closing prices of a stock or portfolio NAV over multiple years

## Notes

- Calculate drawdown as percentage decline from the running maximum: `(value - running_max) / running_max * 100`
- Fill the area from the drawdown line to zero baseline with a semi-transparent color (typically red)
- Highlight the maximum drawdown period with a distinct marker or annotation
- Indicate recovery points where drawdown returns to zero (new highs)
- Display key statistics: maximum drawdown percentage, max drawdown duration, and recovery time
- Zero line should be clearly visible as the reference baseline
- Consider using a secondary y-axis or annotation to show the underlying price/value series
