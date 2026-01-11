# dashboard-metrics-tiles: Real-Time Dashboard Tiles

## Description

A dashboard layout displaying multiple metric tiles in a responsive grid, where each tile shows a KPI value with its label, an embedded sparkline showing recent trend, and a change indicator (up/down arrow with percentage). This visualization is essential for operations monitoring and business dashboards where multiple metrics need to be tracked simultaneously at a glance. The combination of current value, trend visualization, and change direction provides comprehensive metric context in a compact format.

## Applications

- Operations monitoring dashboards displaying server health metrics (CPU, memory, latency)
- Business KPI displays showing sales, revenue, and conversion metrics
- Infrastructure monitoring with real-time system performance indicators
- Marketing analytics dashboards tracking campaign performance metrics

## Data

- `metric_name` (string) - Label/name for each KPI tile
- `current_value` (numeric) - The current/latest value of the metric
- `history` (numeric array) - Historical values for sparkline (10-50 points)
- `change_percent` (numeric) - Percentage change from previous period (positive or negative)
- `status` (categorical, optional) - Status indicator: good, warning, or critical
- Size: 4-12 metric tiles arranged in a grid
- Example: CPU Usage at 45% (down 5%), Memory at 72% (up 8%), Response Time at 120ms (down 15%)

## Notes

- Grid layout should be responsive: 2x2 for 4 tiles, 3x2 for 6 tiles, 3x3 or 4x3 for more
- Each tile contains: prominent value display, metric label, mini sparkline, change indicator with arrow
- Color coding for status: green for good/normal, yellow/orange for warning, red for critical
- Change indicators use up/down arrows with color (green for favorable change, red for unfavorable)
- Sparklines should be compact and positioned below or beside the main value
- Consistent tile sizing and spacing for clean dashboard appearance
- For static output, simulate a snapshot of the real-time state with varied metrics
