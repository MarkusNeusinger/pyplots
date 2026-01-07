# indicator-rsi: RSI Technical Indicator Chart

## Description

A Relative Strength Index (RSI) chart displaying the momentum oscillator on a 0-100 scale with horizontal threshold lines at 70 (overbought) and 30 (oversold). The RSI measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions. This is a fundamental momentum indicator in technical analysis, helping traders identify potential reversal points when the market reaches extreme conditions.

## Applications

- Identifying overbought conditions in stocks when RSI exceeds 70, signaling potential sell opportunities
- Detecting oversold conditions in cryptocurrency markets when RSI drops below 30, indicating potential buying points
- Confirming trend strength and momentum by observing RSI behavior relative to thresholds

## Data

- `date` (datetime) - Trading date or timestamp for each period
- `rsi` (numeric) - RSI value between 0 and 100
- Size: 60-200 periods for meaningful pattern recognition
- Example: Daily RSI values calculated from stock closing prices over 120 trading days using 14-period lookback

## Notes

- Y-axis must be fixed from 0 to 100
- Include horizontal reference lines at 30 (oversold) and 70 (overbought)
- Optionally include a centerline at 50 to show bullish/bearish bias
- RSI line should be clearly visible, typically in a distinct color (e.g., purple or blue)
- Shade or highlight the overbought zone (70-100) and oversold zone (0-30) for visual clarity
- Standard lookback period is 14, but should be noted in the chart
- Typically shown as a separate panel below a price chart, but can stand alone
