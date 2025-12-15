# sparkline-basic: Basic Sparkline

## Description

A sparkline is a small, condensed line chart designed to be embedded inline with text or in dashboard cells. It shows trends at a glance without axes, labels, or detailed scales - pure data visualization in minimal space. The defining characteristic is extreme minimalism: a single continuous line that conveys the shape of data without any chart chrome.

## Applications

- Dashboard KPI trend indicators showing metric changes over time
- Inline stock price trends embedded in financial tables or reports
- Table cells displaying metric history for quick comparison across rows
- Small multiples for comparing many series side-by-side

## Data

- `values` (numeric array) - Sequential values representing the trend to display
- Size: 10-100 data points (enough to show meaningful trends while staying compact)
- Example: Daily sales figures, hourly temperature readings, stock closing prices

## Notes

- No axes, labels, or gridlines - pure visualization
- Compact aspect ratio (wide and short, typically 4:1 to 8:1)
- Optional: highlight min/max points with colored dots
- Optional: highlight first/last points for reference
- Optional: fill under line for area effect
- Line should be thin and clean for clarity at small sizes
