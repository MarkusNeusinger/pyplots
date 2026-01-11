# line-range-buttons: Line Chart with Range Selector Buttons

## Description

A time series line chart featuring preset range selector buttons (1M, 3M, 6M, YTD, 1Y, All) that enable quick navigation to common time periods. The active button is visually highlighted, and the chart smoothly animates when transitioning between ranges. This pattern is ubiquitous in financial platforms and analytics dashboards where users frequently need to compare data across standardized time windows without manual date selection.

## Applications

- Stock price charts in trading platforms with quick access to standard viewing periods
- Performance dashboards tracking KPIs over common business intervals
- Historical data exploration in analytics tools with standardized time comparisons
- Financial reporting interfaces requiring consistent period-over-period analysis

## Data

- `date` (datetime) - Time axis representing the x-coordinate
- `value` (numeric) - Data values representing the y-coordinate
- Size: 1-5 years of daily data (365-1825+ points)
- Example: Daily closing prices, daily revenue figures, or sensor readings over multiple years

## Notes

- Preset buttons: 1M (1 month), 3M (3 months), 6M (6 months), YTD (year to date), 1Y (1 year), All
- Active/selected button should be visually highlighted (different background, border, or color)
- Smooth animation when changing range to provide visual continuity
- Optional: Date range input fields for custom range selection
- Optional: Remember/persist last selected range across sessions
- X-axis date formatting should adapt to selected range (days for 1M, months for 1Y, years for All)
