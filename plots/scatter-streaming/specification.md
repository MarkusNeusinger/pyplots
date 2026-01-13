# scatter-streaming: Streaming Scatter Plot

## Description

A scatter plot that displays data points appearing in real-time, simulating a continuous stream of incoming observations. This visualization is ideal for monitoring live sensor data, event streams, or any scenario where discrete points arrive at a steady rate and need to be visualized as they occur. Unlike animated scatter plots that play through historical data, streaming scatter plots create the effect of watching data arrive live, with new points fading in and old points optionally fading out or being removed from the buffer.

## Applications

- Monitoring live sensor readings (temperature vs. humidity, pressure vs. altitude) from IoT devices
- Visualizing real-time trading ticks with price and volume as coordinates
- Displaying incoming event data (latitude/longitude of transactions, user activity coordinates)
- Tracking experimental measurements arriving from laboratory instruments in real-time

## Data

- `x` (numeric) - Horizontal coordinate of each incoming point
- `y` (numeric) - Vertical coordinate of each incoming point
- `timestamp` (datetime) - Arrival time of each data point, used for ordering and optional color encoding
- Size: 50-500 visible points (with older points removed or faded based on buffer limit)
- Example: Simulated sensor readings arriving at 1-10 points per second, with x/y representing two measured quantities

## Notes

- New points should appear with a fade-in animation effect for smooth visual integration
- Implement a point buffer limit (e.g., keep last N points) to prevent memory issues and maintain readability
- Optional point trail/history fading where older points become more transparent before removal
- Support both auto-scaling axes (adapting to data range) and fixed bounds (predetermined axis limits)
- Optional timestamp-based coloring to show recency (newer points brighter or different hue)
- For static image output, show a snapshot with visual indication of data flow (e.g., opacity gradient from old to new points)
- Libraries without animation support should show a static view with opacity encoding for point age
