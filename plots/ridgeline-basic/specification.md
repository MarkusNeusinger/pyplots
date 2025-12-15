# ridgeline-basic: Basic Ridgeline Plot

## Description

A ridgeline plot (also known as Joy Plot, named after the Joy Division album cover) displays the distribution of multiple groups by stacking partially overlapping density curves vertically. This creates a mountain ridge appearance that allows efficient comparison of many distributions simultaneously while maintaining a compact and visually striking presentation.

## Applications

- Comparing temperature distributions across months to reveal seasonal patterns
- Analyzing survey response distributions by demographic segments
- Visualizing population age distributions across different regions or time periods
- Showing how performance metrics vary across different teams or time windows

## Data

- `value` (numeric) - The continuous variable to visualize as density curves
- `group` (categorical) - The grouping variable that creates separate ridges (5-20 groups recommended)
- Size: 50-500 observations per group for smooth density estimation
- Example: Monthly temperature readings, survey scores by age group, reaction times by condition

## Notes

- Stack density curves vertically with partial overlap (typically 50-70% overlap)
- Y-axis should display group labels rather than numeric values
- Consider color gradients or distinct colors to differentiate ridges
- Ensure sufficient overlap for visual cohesion while maintaining readability
- Order groups meaningfully (chronological, alphabetical, or by distribution characteristic)
