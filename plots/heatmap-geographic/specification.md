# heatmap-geographic: Geographic Heatmap for Spatial Density

## Description

A geographic heatmap visualizes spatial density or intensity values across a map using continuous color gradients. Unlike choropleth maps that color discrete regions, this plot shows smooth density variations computed from point data or gridded values. The color intensity at each location represents the concentration or magnitude of the underlying data, making it ideal for identifying hotspots, clusters, and spatial patterns in geographic data.

## Applications

- Visualizing crime incident density across a city to identify high-risk areas
- Mapping population or activity density in urban planning studies
- Displaying temperature, pollution, or environmental measurements interpolated across a geographic region
- Showing customer or event density for retail site selection and marketing analysis

## Data

- `latitude` (numeric) - Geographic latitude coordinate (-90 to 90)
- `longitude` (numeric) - Geographic longitude coordinate (-180 to 180)
- `value` (numeric, optional) - Intensity or weight value at each point (defaults to 1 for pure density)
- Size: 100-10,000 points (density estimation works best with sufficient data coverage)
- Example: GPS coordinates of events, sensor locations with measurement values, or activity locations

## Notes

- Use kernel density estimation (KDE) or similar interpolation to create the continuous heatmap layer
- Apply a sequential colormap (e.g., YlOrRd, inferno) with transparency to allow the basemap to show through
- Include a colorbar legend showing the density or intensity scale
- Add geographic context with country boundaries, coastlines, or street maps as a basemap
- Consider adjusting the bandwidth/radius parameter based on data density and geographic scale
- For interactive libraries, enable zoom to explore density at different scales
