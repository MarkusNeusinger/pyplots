# bullet-basic: Basic Bullet Chart

## Description

A bullet chart displays a single measure against qualitative ranges and a target marker, designed by Stephen Few as a space-efficient alternative to gauge charts. The linear format shows actual performance as a bar, a target as a vertical marker, and background bands representing qualitative ranges (poor/satisfactory/good). Its compact design allows multiple bullet charts to fit on a single dashboard for easy comparison across metrics.

## Applications

- Displaying sales performance against quarterly quotas in executive dashboards
- Showing project completion percentage against milestone targets in PMO reports
- Comparing actual vs budgeted expenses across departments in financial reviews
- Visualizing quality metrics (defect rates, SLA compliance) against acceptable thresholds

## Data

- `actual` (numeric) - The current/measured value to display as the primary bar
- `target` (numeric) - The goal or target value shown as a vertical marker line
- `ranges` (list of numeric) - Thresholds defining qualitative bands (e.g., [50, 75, 100] for poor/satisfactory/good)
- `label` (string, optional) - Category or metric name for the bullet chart
- Size: Single value display per bullet; multiple bullets can be stacked vertically
- Example: actual = 75, target = 90, ranges = [50, 75, 100] for a KPI at 75% with 90% target

## Notes

- Use grayscale shading for background bands to keep focus on the primary measure bar
- The target marker should be a thin contrasting line (often black) perpendicular to the bar
- Horizontal orientation is most common; vertical can be used when space requires it
- Consider adding the actual value as a text label for precise reading
- Multiple bullet charts should align on a common scale when comparing related metrics
