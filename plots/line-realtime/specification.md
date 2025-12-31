# line-realtime: Real-Time Updating Line Chart

## Description

A line chart that simulates real-time data updates, with new points being added dynamically and the chart scrolling or animating to show the latest values. This visualization is essential for monitoring scenarios where data streams continuously and users need to observe trends as they happen. Unlike static time series plots, real-time charts create the effect of live data flow through animation and a sliding time window.

## Applications

- Monitoring server CPU, memory, or network utilization in a dashboard with updates every second
- Visualizing live sensor readings (temperature, pressure, heart rate) from IoT devices
- Tracking live stock prices or cryptocurrency values with automatic chart updates

## Data

- `timestamp` (datetime) - Time value for each data point, representing when the observation occurred
- `value` (numeric) - The measured quantity at each timestamp
- Size: 50-200 visible points (with older points scrolling off-screen)
- Example: Simulated CPU usage percentages sampled every 100ms, live temperature readings from a sensor

## Notes

- Implement a sliding window that shows only the most recent N data points or time period
- Use smooth animations when adding new points and scrolling the view
- Consider using requestAnimationFrame or library-specific animation methods for fluid updates
- Include axis labels that update dynamically as the time window shifts
- Add a legend or label showing the current/latest value prominently
- For static image output, show a snapshot with visual indication of the scrolling direction (e.g., arrow or fade effect on trailing edge)
