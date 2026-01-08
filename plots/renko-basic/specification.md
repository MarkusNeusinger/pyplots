# renko-basic: Basic Renko Chart

## Description

A Renko chart displays price movements using fixed-size bricks that ignore time and focus purely on price action. A new brick is drawn only when the price moves by a specified amount (brick size), filtering out market noise and minor fluctuations. Bullish bricks (price increase) and bearish bricks (price decrease) alternate direction on trend reversals, making it easy to identify trends, support/resistance levels, and potential trading signals.

## Applications

- Identifying clear trend directions in stock prices by filtering out intraday noise and focusing on significant price movements
- Spotting support and resistance levels in forex trading where price repeatedly reverses at certain brick levels
- Generating cleaner trading signals by removing time-based volatility from cryptocurrency price analysis

## Data

- `date` (datetime) - The timestamp when each price point was recorded
- `close` (numeric) - Closing price or last traded price at each timestamp
- Brick size: A fixed price amount that determines when a new brick is drawn (e.g., $1, $5, or percentage-based)
- Size: 100-500 price observations to generate 20-50 meaningful bricks
- Example: Daily closing prices for a stock over 6 months with a $2 brick size

## Notes

- Use green/up color for bullish bricks and red/down color for bearish bricks
- Bricks should be uniform in size and clearly separated with a small gap
- X-axis can show brick index or estimated date ranges (since time is irregular)
- Consider adding a subtle grid to help identify price levels
- The brick size significantly affects the chart appearance - smaller bricks show more detail, larger bricks show broader trends
