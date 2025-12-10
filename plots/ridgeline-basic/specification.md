# ridgeline-basic: Ridgeline Plot

## Description

A ridgeline plot (also known as joy plot) displays multiple overlapping density distributions arranged vertically, allowing effective comparison of distributions across categories. Each distribution is plotted as a filled density curve, slightly overlapping with adjacent rows to create a visually appealing layered effect. This visualization excels at revealing distribution shapes, modes, and shifts across groups.

## Applications

- Comparing salary distributions across different job titles to identify compensation patterns
- Visualizing temperature distributions across months to show seasonal climate patterns
- Showing survey response distributions by demographic groups to understand opinion variations

## Data

- `category` (categorical) - grouping variable for vertical arrangement (y-axis labels)
- `value` (numeric, continuous) - the variable whose distribution is shown (x-axis)
- Size: 5-20 categories, 50-500+ observations per category
- Example: Monthly temperature readings with month as category and temperature as value

## Notes

- Distributions should overlap slightly (10-30%) for visual appeal without obscuring data
- Use semi-transparent fills (alpha 0.6-0.8) to maintain visibility of overlapping areas
- Named after the Joy Division album cover "Unknown Pleasures" featuring pulsar radio signals
- Consider gradient coloring from bottom to top for additional visual interest
- Kernel density estimation (KDE) is typically used to smooth the distributions
