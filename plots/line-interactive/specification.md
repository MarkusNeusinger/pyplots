# line-interactive: Interactive Line Chart with Hover and Zoom

## Description

An interactive line chart that enables detailed data exploration through hover tooltips, zoom/pan functionality, and range selection. Unlike static line charts, this visualization allows users to examine exact values on hover, zoom into areas of interest, and select time ranges for focused analysis. It excels at making large time series accessible and revealing fine-grained patterns that would be lost in static views.

## Applications

- Exploring financial data with ability to zoom into specific trading periods and see exact prices
- Analyzing sensor data or IoT metrics where users need to drill down into anomalies
- Interactive dashboards for monitoring website traffic with range selection for period comparison

## Data

- `x` (numeric/datetime) - Sequential or time values representing the independent variable
- `y` (numeric) - Continuous values representing the measured quantity
- Size: 50-1000+ points (interactivity handles larger datasets well)
- Example: Stock prices over time, hourly server metrics, daily temperature readings

## Notes

- Hover tooltips should display exact x and y values with appropriate formatting
- Zoom should support both mouse wheel and click-drag box selection
- Pan functionality for navigating zoomed views
- Range selector or slider for quick navigation of time series
- Reset zoom button to return to full view
- Smooth animations for zoom/pan transitions enhance user experience
