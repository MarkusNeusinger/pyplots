# indicator-ema: Exponential Moving Average (EMA) Indicator Chart

## Description

An Exponential Moving Average (EMA) overlay chart displays price data with one or more EMA lines that give greater weight to recent prices, making them more responsive to new information than simple moving averages. The EMA calculation applies an exponential weighting factor that decreases with each older data point, allowing traders to identify trends faster. This technical indicator is fundamental in trading for spotting trend direction, dynamic support/resistance levels, and crossover signals.

## Applications

- Identifying trend direction in stock prices using 50-day and 200-day EMA crossovers (golden cross/death cross signals)
- Detecting short-term momentum shifts in cryptocurrency trading using fast EMAs (12, 26 periods)
- Generating entry/exit signals when price crosses above or below EMA lines in forex trading

## Data

- `date` (datetime) - Trading date or timestamp for each period
- `close` (numeric) - Closing price for each period
- `ema_short` (numeric) - Short-period EMA value (e.g., 12-day or 26-day)
- `ema_long` (numeric) - Long-period EMA value (e.g., 50-day)
- Size: 60-200 periods for meaningful trend visualization
- Example: Daily stock prices with 12-day and 26-day EMAs over 120 trading days

## Notes

- Display the price line prominently (line or candlestick) with EMA lines overlaid
- Use distinct colors for each EMA period (e.g., short EMA in blue, long EMA in orange)
- EMA lines should be slightly thinner than the price line to avoid visual clutter
- Common periods to display: 12, 26 (short-term), 50, 200 (long-term)
- Consider highlighting crossover points where short EMA crosses long EMA
- Label each EMA line with its period in the legend
