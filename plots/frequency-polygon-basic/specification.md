# frequency-polygon-basic: Frequency Polygon for Distribution Comparison

## Description

A frequency polygon connects the midpoints of histogram bins with straight line segments, creating a smooth outline of the distribution shape. This visualization excels at comparing multiple distributions simultaneously since lines overlap without obscuring each other, unlike stacked or overlapping histogram bars. Frequency polygons reveal differences in central tendency, spread, skewness, and modality across groups with minimal visual clutter.

## Applications

- Comparing test score distributions across multiple classes or exam sessions
- Analyzing response time distributions between experimental conditions in psychology research
- Visualizing age distributions across different customer segments or cohorts

## Data

- `values` (numeric) - The continuous variable to bin and display
- `group` (categorical) - The grouping variable distinguishing each distribution
- Size: 50-1000 observations per group recommended; works well with 2-5 groups
- Example: Heights by age group, salaries by department, reaction times by treatment

## Notes

- Use distinct line colors and/or styles (solid, dashed) to differentiate groups
- Include a legend clearly identifying each group
- Consider adding markers at data points for small datasets
- Extend lines to zero at both ends to close the polygon shape
- Align bin edges across all groups for accurate comparison
- Semi-transparent fill beneath lines can enhance visual appeal while preserving clarity
