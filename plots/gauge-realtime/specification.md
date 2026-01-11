# gauge-realtime: Real-Time Updating Gauge

## Description

A gauge chart that simulates real-time data updates with smooth animated transitions between values. The needle or arc indicator moves fluidly to new positions, creating the effect of live metric monitoring. This visualization is essential for dashboards where users need to observe metric fluctuations as they happen, combining the intuitive speedometer metaphor with dynamic updating behavior.

## Applications

- Monitoring server CPU and memory utilization with live percentage updates in DevOps dashboards
- Displaying real-time KPI values (conversion rates, active users) in business intelligence dashboards
- Visualizing IoT sensor readings (temperature, pressure, humidity) with continuous updates
- Showing live performance metrics during load testing or system benchmarking

## Data

- `value` (numeric) - The current metric value to display on the gauge
- `min_value` (numeric) - The minimum value of the gauge range (default: 0)
- `max_value` (numeric) - The maximum value of the gauge range (default: 100)
- `thresholds` (list of numeric, optional) - Boundaries for color zones (e.g., [30, 70] creates green/yellow/red zones)
- Update frequency: 1-5 seconds between value changes
- Example: Simulated CPU usage fluctuating between 20-95%, with thresholds at 50 and 80 for status indication

## Notes

- Implement smooth animation when the needle or arc transitions between values
- Use color zones (green/yellow/red) following intuitive conventions where green indicates acceptable and red indicates critical
- Display the current value prominently as a numeric label
- Include min and max labels at the gauge boundaries
- For static image output, show a snapshot with visual indication of the dynamic nature (e.g., motion blur effect or multiple needle positions)
- Simulated updates should use realistic value changes (not random jumps) to demonstrate smooth transitions
