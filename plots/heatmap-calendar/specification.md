# heatmap-calendar: Basic Calendar Heatmap

## Description

A calendar heatmap visualizes time-series data on a calendar grid, where each day is represented as a cell and color intensity indicates the value magnitude. The layout follows a calendar structure with days as cells, weeks as rows, and months as columns or sections. This visualization excels at revealing daily patterns, seasonal trends, and temporal anomalies over extended time periods.

## Applications

- GitHub-style contribution graphs showing daily coding activity
- Daily sales or website traffic patterns across months
- Habit tracking visualization for personal productivity
- Weather data patterns showing temperature or precipitation by day

## Data

- `date` (datetime) - daily dates covering the time range
- `value` (numeric) - measurement or count for each day
- Size: 365-730 days (1-2 years) for optimal readability
- Example: daily commit counts, step counts, or temperature readings

## Notes

- Display weekday labels (Mon-Sun) on the y-axis
- Show month labels along the top or as section headers
- Use a sequential colormap (light to dark) for positive values
- Handle missing dates gracefully with neutral or empty cells
- Include a color scale legend for value interpretation
