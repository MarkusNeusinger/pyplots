# step-basic: Basic Step Plot

## Description

A step plot (also known as a stair plot or stepped line chart) displays data using horizontal lines connected by vertical lines, creating a stair-step pattern. Unlike line charts that interpolate between points, step plots show values as constant until the next change occurs. This makes them ideal for visualizing data that changes at discrete intervals, emphasizing the exact moments when values change.

## Applications

- Tracking cumulative sales or revenue over time where totals increase in discrete jumps
- Visualizing stock price changes or pricing tier adjustments throughout a trading day
- Displaying inventory levels that decrease or increase at specific events
- Showing digital signals, binary states, or step functions in engineering and mathematics

## Data

- `x` (numeric/datetime) - Sequential or time-based variable representing when changes occur
- `y` (numeric) - The value that remains constant until the next step
- Size: 10-100 data points work well; too many points may clutter the visualization
- Example: Monthly cumulative sales figures, hourly inventory snapshots

## Notes

- Use 'pre' step style when the value applies from the previous point until the current one
- Use 'post' step style when the value applies from the current point until the next one
- Use 'mid' step style to center the step between adjacent points
- Consider adding markers at data points to highlight where changes occur
- Grid lines can help readers trace values across the plot
