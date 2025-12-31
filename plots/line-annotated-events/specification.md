# line-annotated-events: Annotated Line Plot with Event Markers

## Description

A line plot with annotations at key points marking important events or milestones. This visualization enhances time series data by highlighting significant occurrences such as product launches, policy changes, or market events directly on the chart. Vertical lines, markers, and text labels draw attention to specific moments in time, making it easy to correlate data trends with real-world events.

## Applications

- Marking earnings announcements, dividends, or splits on a stock price chart
- Highlighting product releases or feature launches on user growth metrics
- Annotating policy changes or regulatory events on economic indicators
- Indicating equipment failures or maintenance windows on sensor data

## Data

- `date` (datetime) - Timestamp values for the continuous time series
- `value` (numeric) - Continuous measurements or observations at each timestamp
- `event_date` (datetime) - Timestamps of significant events to mark
- `event_label` (string) - Text description for each event marker
- Size: 50-500 points for the main series, 3-10 event markers
- Example: Daily stock prices over a year with quarterly earnings dates marked

## Notes

- Use vertical lines (axvline) to mark event dates clearly
- Position event labels to avoid overlapping with data or each other
- Consider rotating labels or using alternating heights for dense event clusters
- Event markers should be visually distinct from the data line (different color, dashed)
- Include a subtle legend or key if multiple event types are shown
