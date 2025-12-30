# line-timeseries-rolling: Time Series with Rolling Average Overlay

## Description

A time series plot that displays raw data points alongside a smoothed rolling average (moving average) line. The raw data shows actual observations while the rolling average reveals underlying trends by reducing noise and short-term fluctuations. This dual-layer visualization is essential for trend identification, making patterns visible that might be obscured by day-to-day volatility.

## Applications

- Analyzing stock price movements with a moving average to identify buy/sell signals and trend reversals
- Monitoring website traffic or user engagement metrics with smoothed trends for seasonal pattern detection
- Tracking sensor data (temperature, humidity) with noise reduction to reveal true environmental trends

## Data

- `date` (datetime) - Timestamp values representing points in time
- `value` (numeric) - Raw measurements or observations at each timestamp
- `rolling_avg` (numeric) - Computed rolling average (e.g., 7-day, 30-day window)
- Size: 50-500 points (enough data for meaningful rolling window calculation)
- Example: Daily stock closing prices with 20-day moving average, hourly temperature readings with 24-hour rolling mean

## Notes

- Use a lighter, semi-transparent style for raw data (thin line or markers with alpha)
- Display the rolling average as a prominent, smooth line in a contrasting color
- Include a legend clearly distinguishing "Raw Data" from "Rolling Average (N-day)"
- Consider showing the window size in the legend or title (e.g., "7-Day Rolling Average")
- Grid lines on both axes improve readability of underlying values
- The rolling average line will be shorter than raw data due to window requirements
