# candlestick-volume: Stock Candlestick Chart with Volume

## Description

A professional candlestick chart combining OHLC (open, high, low, close) price data with volume bars in a synchronized lower pane. The dual-pane layout presents price action in the main chart with corresponding trading volume below, sharing a common time axis. This format is the standard for technical analysis platforms, enabling traders to correlate price movements with trading activity and identify volume-confirmed trends or reversals.

## Applications

- Analyzing stock price movements alongside trading volume to confirm breakout patterns
- Identifying divergences between price trends and volume for potential reversal signals
- Evaluating cryptocurrency or forex pairs with volume context for entry/exit decisions

## Data

- `date` (datetime) - Trading date or timestamp for each period
- `open` (numeric) - Opening price at the start of the period
- `high` (numeric) - Highest price during the period
- `low` (numeric) - Lowest price during the period
- `close` (numeric) - Closing price at the end of the period
- `volume` (numeric) - Number of shares or units traded during the period
- Size: 30-120 periods for clear visualization without overcrowding
- Example: Daily OHLC data with volume for a stock over 60 trading days

## Notes

- Use a shared x-axis between the candlestick and volume panes with proper date formatting
- Volume bars should use the same up/down color scheme as candlesticks for visual consistency
- The price pane should occupy roughly 70-75% of the vertical space, volume pane 25-30%
- Include a crosshair or cursor that spans both panes for precise price/volume reading
- Grid lines should be subtle and aligned across both panes
