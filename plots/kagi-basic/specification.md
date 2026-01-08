# kagi-basic: Basic Kagi Chart

## Description

A Kagi chart is a Japanese charting technique that displays price movements using vertical lines of varying thickness. Unlike time-based charts, Kagi charts change direction only when price moves by a significant amount (the reversal threshold), effectively filtering out market noise. Thick lines (yang) indicate uptrends when price exceeds previous highs, while thin lines (yin) show downtrends when price falls below previous lows, making trend identification intuitive.

## Applications

- Identifying clear trend reversals in stock trading by observing when thick lines transition to thin lines or vice versa
- Analyzing currency pair movements in forex markets where filtering out minor fluctuations helps spot major trend changes
- Evaluating cryptocurrency price action over extended periods by focusing on significant price movements rather than time-based volatility

## Data

- `date` (datetime) - The timestamp when each price point was recorded
- `close` (numeric) - Closing price or last traded price at each timestamp
- Reversal amount: A fixed price or percentage threshold that triggers a direction change (e.g., $2 or 4%)
- Size: 100-500 price observations to generate meaningful trend patterns
- Example: Daily closing prices for a stock over 6-12 months with a 4% reversal threshold

## Notes

- Use thick lines for yang (bullish) segments and thin lines for yin (bearish) segments
- Direction changes occur only when price moves by the reversal amount in the opposite direction
- Horizontal segments (shoulders and waists) mark the points where trend direction changes
- Green color for yang (thick/up) and red color for yin (thin/down) provides visual clarity
- X-axis typically shows line index rather than time since Kagi charts are time-independent
- The reversal threshold significantly impacts chart appearance - smaller values show more detail, larger values emphasize major trends
