# violin-swarm: Violin Plot with Overlaid Swarm Points

## Description

A violin plot with individual data points overlaid as a swarm plot, combining smooth kernel density estimation with raw data visibility. The violin shape shows the distribution density while the swarm points reveal actual observations, enabling viewers to see both the overall distribution pattern and individual data values simultaneously. This hybrid approach provides maximum transparency, showing exactly how many observations exist at each level while maintaining the smooth distribution visualization.

## Applications

- Comparing gene expression levels across treatment conditions in biological research
- Analyzing response time distributions across experimental groups while showing individual trials
- Visualizing patient biomarker values across clinical groups with full data transparency
- Presenting survey response distributions where sample sizes vary between groups

## Data

- `category` (categorical) - Group labels for comparison on the categorical axis
- `value` (numeric) - Continuous variable values shown on the value axis
- Size: 20-200 observations per category, 2-5 categories
- Example: Reaction times (ms) across 4 experimental conditions with 50 observations each

## Notes

- Overlay swarm points on top of the violin, centered within the violin shape
- Use transparency on the violin (alpha 0.3-0.5) so swarm points remain visible
- Size swarm points appropriately to avoid excessive overlap while remaining visible
- Consider using a contrasting color for points vs violin fill
- Swarm points should spread horizontally to avoid overlap, staying within the violin boundary
