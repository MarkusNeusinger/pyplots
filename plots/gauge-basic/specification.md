# gauge-basic: Basic Gauge Chart

## Description

A gauge chart (also known as a speedometer chart) displays a single value within a defined range using a semi-circular or circular dial. It is ideal for showing progress toward a goal, performance metrics, or any KPI that needs to be evaluated against minimum and maximum bounds. The visual metaphor of a speedometer makes it intuitive to quickly assess whether a value is in an acceptable range.

## Applications

- Displaying a company's quarterly revenue against annual targets in executive dashboards
- Showing CPU or memory utilization percentage in system monitoring tools
- Visualizing customer satisfaction scores or Net Promoter Scores (NPS) in business analytics
- Indicating completion percentage for project milestones or fundraising goals

## Data

- `value` (numeric) - The current value to display on the gauge
- `min_value` (numeric) - The minimum value of the gauge range (default: 0)
- `max_value` (numeric) - The maximum value of the gauge range (default: 100)
- `thresholds` (list of numeric, optional) - Boundaries for color zones (e.g., [30, 70] creates three zones)
- Size: Single value display
- Example: Current sales = 72, min = 0, max = 100, thresholds at 30 and 70 for red/yellow/green zones

## Notes

- Use a semi-circular gauge for dashboard widgets where vertical space is limited
- Color zones (red/yellow/green) should follow intuitive conventions (red = bad, green = good)
- Display the current value prominently as a label, typically centered below the gauge
- The needle or arc indicator should clearly point to the current value position
