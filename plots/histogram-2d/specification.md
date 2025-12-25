# histogram-2d: 2D Histogram Heatmap

## Description

A two-dimensional histogram that displays the joint distribution of two continuous variables as a heatmap with rectangular bins. Each bin's color intensity represents the frequency or count of data points falling within that region, making it ideal for revealing density patterns, clusters, and correlations in bivariate data. Unlike scatter plots that can become cluttered with large datasets, 2D histograms effectively summarize point density.

## Applications

- Analyzing joint distributions of financial returns across different asset classes
- Visualizing particle collision data density in physics experiments
- Exploring the relationship between customer age and purchase frequency in market research
- Identifying spatial density patterns in geographic coordinate data

## Data

- `x` (numeric) - continuous values for the horizontal axis
- `y` (numeric) - continuous values for the vertical axis
- Size: 500-100,000+ points (designed for datasets where scatter plots become unreadable)
- Example: Bivariate normal distribution with correlation

## Notes

- Include a colorbar to show the density/count scale
- Use a perceptually uniform colormap (e.g., viridis) for accurate density interpretation
- Bins parameter controls resolution (more bins = finer detail but noisier)
- Consider log scale for color mapping when density varies widely
- Optional: add marginal 1D histograms on top and right edges for univariate context
