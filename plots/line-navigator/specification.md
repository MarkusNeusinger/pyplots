# line-navigator: Line Chart with Mini Navigator

## Description

A line chart featuring a miniature overview pane at the bottom that serves as a navigator for exploring large time series datasets. The main chart displays the selected range in detail while the mini chart below shows the full data extent with a draggable selection window. Users can resize the selection handles to adjust the visible range, enabling intuitive exploration of long time series with smooth zoom transitions between the overview and detail views.

## Applications

- Exploring long time series data spanning months or years while maintaining context of the full history
- Stock chart analysis with a history overview for navigating between different market periods
- Sensor data visualization with zoom capability to investigate specific anomalies or patterns
- Log file timeline navigation to quickly jump between different time ranges while seeing overall activity

## Data

- `date` (datetime) - Time axis representing the temporal dimension
- `value` (numeric) - Data values to be visualized as a continuous line
- Size: 1000+ data points (designed for large datasets where navigation is essential)
- Example: Daily sensor readings over multiple years, hourly stock prices, system metrics over time

## Notes

- Main chart shows the selected range in full detail with appropriate axis formatting
- Mini chart below displays the entire data extent at reduced scale
- Draggable selection window in the navigator highlights the currently visible range
- Resize handles on selection edges for fine-grained range adjustment
- Smooth animated transitions when changing the selected range
- Both charts should share the same styling (line color, thickness) for visual consistency
- Navigator height should be proportionally smaller (15-20% of main chart height)
- Consider showing the selected date range as text labels
