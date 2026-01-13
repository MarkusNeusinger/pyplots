# map-projections: World Map with Different Projections

## Description

A world map demonstrating different cartographic projections and their distortion characteristics. This visualization showcases how the same geographic data appears under various map projections (Mercator, Robinson, Mollweide, Orthographic, etc.), revealing how each projection preserves or distorts area, shape, distance, or direction. The plot includes graticule (latitude/longitude grid lines) and optionally Tissot indicatrices to illustrate projection distortion patterns.

## Applications

- Educational cartography demonstrating how map projections transform the spherical Earth to a flat surface
- Comparing projection suitability for different geographic analyses or presentations
- Visualizing global data with area-accurate projections to avoid misleading size comparisons
- Teaching geographic information systems (GIS) concepts about coordinate reference systems

## Data

- World country boundaries (GeoJSON format or shapefile)
- `country` (string) - Country identifier or ISO code
- `value` (numeric, optional) - Data variable for choropleth coloring
- Size: ~200 countries (world boundaries dataset)
- Example: Natural Earth world boundaries, country-level statistics

## Notes

- Support multiple projections: Mercator, Robinson, Mollweide, Orthographic, Equal Earth, Lambert Cylindrical, or other common projections
- Display graticule (latitude/longitude grid lines) at regular intervals (e.g., every 30 degrees)
- Show clean coastlines and country borders with appropriate styling
- Optional: Include Tissot indicatrices (circles that show distortion) to visualize how the projection affects area and shape
- Use a neutral color scheme for land masses when not showing data values
- Consider showing the same map in multiple projections side-by-side for comparison, or a single projection with clear title indicating which one
