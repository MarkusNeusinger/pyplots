# indicator-macd: MACD Technical Indicator Chart

## Description

A MACD (Moving Average Convergence Divergence) chart displaying three components: the MACD line, signal line, and histogram. The MACD line represents the difference between 12-day and 26-day exponential moving averages, while the signal line is a 9-day EMA of the MACD. The histogram visualizes the difference between these two lines. This is an essential momentum oscillator for technical analysis, helping traders identify trend direction, momentum strength, and potential buy/sell signals through line crossovers.

## Applications

- Analyzing stock price momentum to identify trend reversals and entry/exit points
- Generating trading signals for cryptocurrency markets based on MACD/signal line crossovers
- Confirming trend strength by observing histogram expansion or contraction

## Data

- `date` (datetime) - Trading date or timestamp for each period
- `macd` (numeric) - MACD line value (12-day EMA minus 26-day EMA)
- `signal` (numeric) - Signal line value (9-day EMA of MACD)
- `histogram` (numeric) - Difference between MACD and signal line
- Size: 60-200 periods for meaningful pattern recognition
- Example: Daily MACD values calculated from stock closing prices over 120 trading days

## Notes

- Display histogram as bars with green (positive) and red (negative) colors
- Include a zero reference line to highlight crossover signals
- MACD and signal lines should use distinct colors (e.g., blue and orange)
- Standard parameters are 12, 26, 9 but should be noted in the chart
- Typically shown as a separate panel below a price chart, but can stand alone
