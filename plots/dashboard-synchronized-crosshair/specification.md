# dashboard-synchronized-crosshair: Synchronized Multi-Chart Dashboard

## Description

A multi-chart dashboard layout where hovering over one chart displays synchronized crosshairs and tooltips across all other charts at the same x-axis position. This interaction pattern is essential for comparing multiple related metrics over a shared time axis, allowing users to instantly see how different variables relate at any given point. The vertical crosshair line spans all charts simultaneously, while tooltips display values from each chart at the hover position.

## Applications

- Multi-indicator financial analysis comparing price, volume, RSI, and MACD with synchronized cursors for correlated signal detection
- Correlated time series comparison in scientific research where multiple measurements share a common timeline
- Operations dashboards linking CPU, memory, network, and disk metrics with unified hover inspection
- Exploratory data analysis with linked views for discovering temporal relationships across variables

## Data

- `date` (datetime) - Shared time axis for all charts
- `series_1` (numeric) - Values for the first chart (e.g., price)
- `series_2` (numeric) - Values for the second chart (e.g., volume)
- `series_3` (numeric) - Values for the third chart (e.g., indicator)
- Size: 100-500 time points for responsive interactivity
- Example: Stock data with price, volume, and technical indicators over 200 trading days

## Notes

- Synchronized vertical crosshair line that spans all charts at the hover position
- Shared tooltip showing values from all series at the current x-position
- Stacked vertical layout with charts sharing a common x-axis
- Synchronized zoom and pan across all charts when supported by the library
- Independent y-axis scales for each chart to accommodate different value ranges
- Clear visual connection between charts (shared axis, aligned grids)
- For static libraries, demonstrate the layout structure with annotations; for interactive libraries, implement full crosshair synchronization
