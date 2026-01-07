# bar-interactive: Interactive Bar Chart with Hover and Click

## Description

An interactive bar chart that enables data exploration through hover tooltips displaying detailed values and click interactions for drill-down or filtering. This visualization extends static bar charts with user engagement features, allowing viewers to examine exact values on hover and trigger actions through clicks. It excels in dashboards and exploratory interfaces where users need to interact with categorical data.

## Applications

- Dashboard data exploration with drill-down capability into subcategories
- Sales reports allowing click-through to detailed transaction views
- Survey results with hover tooltips showing response percentages and counts
- Performance metrics comparison with click-to-filter functionality
- Budget allocation visualization with interactive category breakdowns

## Data

- `category` (categorical) - Discrete labels for the x-axis representing different groups
- `value` (numeric) - Heights of the bars representing the measured quantity
- `tooltip_data` (optional) - Additional fields to display in hover tooltips (percentages, counts, labels)
- `click_target` (optional) - URLs, filter values, or identifiers for click actions
- Size: 3-20 categories recommended for optimal interactivity
- Example: Product sales with drill-down to regional data, survey responses with demographic breakdowns

## Notes

- Hover tooltips should display: category name, primary value, and optional additional data
- Visual feedback on hover is essential: highlight, color change, or slight enlargement
- Click actions can include: drill-down to detail view, apply filter, navigate to URL, or trigger callback
- Best suited for interactive libraries: plotly, bokeh, altair, highcharts, letsplot
- Consider cursor change on hover to indicate clickability
- Animations for hover transitions enhance perceived interactivity
