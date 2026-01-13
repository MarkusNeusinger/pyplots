# map-tile-background: Map with Tile Background

## Description

A map visualization that displays data points on top of tile-based backgrounds such as OpenStreetMap, Stamen, or satellite imagery. Unlike vector-based basemaps, tile backgrounds provide rich geographic context including street-level detail, terrain, or satellite imagery that loads dynamically as the user navigates. This visualization is essential for location-based analysis where real-world geographic context enhances data interpretation.

## Applications

- Visualizing location-based business data (store locations, service areas) with street-level context
- Plotting GPS tracks or routes on real maps for navigation and transportation analysis
- Displaying sensor or IoT device locations with surrounding terrain and infrastructure
- Analyzing urban vs rural patterns with satellite imagery providing land use context

## Data

- `lat` (numeric) - Latitude coordinate for each point (-90 to 90)
- `lon` (numeric) - Longitude coordinate for each point (-180 to 180)
- `value` (numeric, optional) - Data value for color or size encoding
- `label` (string, optional) - Text label or identifier for each point
- Size: 10-500 points (tile maps work well with moderate point density)
- Example: City landmarks with visitor counts, delivery locations with order values

## Notes

- Support multiple tile providers (OpenStreetMap, Stamen Terrain/Toner, CartoDB, satellite)
- Set appropriate initial zoom level based on data extent (auto-fit to data bounds)
- Layer data markers on top of tiles with sufficient contrast and optional outline
- Include proper attribution for tile providers as required by their terms of use
- For interactive libraries, enable zoom and pan to explore data at different scales
- Consider marker clustering for dense point distributions at low zoom levels
