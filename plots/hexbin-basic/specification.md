# hexbin-basic: Basic Hexbin Plot

## Description

A hexagonal binning plot that visualizes the density of 2D point data by aggregating points into hexagonal bins. The color intensity of each hexagon represents the count of points within it, making it ideal for revealing density patterns in large datasets where traditional scatter plots would show overlapping points. Hexagonal bins provide better visual representation than square pixels due to their isotropy (equal distance to neighboring cells in all directions).

## Applications

- Visualizing millions of GPS coordinates to identify traffic hotspots or popular locations in urban analytics
- Analyzing financial tick data to find price-volume density clusters in trading patterns
- Exploring sensor readings from IoT devices to detect concentration patterns in environmental monitoring
- Identifying user interaction hotspots in click-stream or eye-tracking data analysis

## Data

- `x` (numeric) - X-axis coordinate values
- `y` (numeric) - Y-axis coordinate values
- Size: 1,000-1,000,000+ points (designed for large datasets where scatter plots become unreadable)
- Example: Randomly generated bivariate data with clustered distribution

## Notes

- Include a color bar to show the density scale
- Use a perceptually uniform colormap (e.g., viridis) for accurate density interpretation
- Gridsize parameter controls bin resolution (higher = smaller hexagons, more detail)
- Consider log scale for color mapping when density varies widely
