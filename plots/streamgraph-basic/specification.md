# streamgraph-basic: Basic Stream Graph

## Description

A streamgraph (also known as a stacked area chart with a centered baseline) displaying the composition of multiple categories over time with smooth, flowing curves. Unlike traditional stacked area charts, streamgraphs use a symmetric baseline centered around the x-axis, creating an organic, river-like appearance that emphasizes the overall shape and relative proportions of each category while minimizing the visual distortion of individual layers.

## Applications

- Music listening trends showing genre popularity over months
- Topic popularity evolution in social media or news
- Market share changes among competitors over time
- Resource allocation across teams or projects over quarters

## Data

- `time` (datetime/numeric) - continuous time axis for the x-dimension
- `category` (categorical) - distinct categories/series to stack
- `value` (numeric) - magnitude for each category at each time point
- Size: 10-100 time points with 3-8 categories
- Example: monthly streaming hours by music genre over two years

## Notes

- Use smooth interpolation (spline/basis) for flowing curves
- Center the baseline symmetrically around the x-axis
- Use distinct, harmonious colors for each category
- Include a legend to identify categories
- Consider color palette that works well for adjacent areas
