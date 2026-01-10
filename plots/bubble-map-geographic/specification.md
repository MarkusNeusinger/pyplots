# bubble-map-geographic: Bubble Map with Sized Geographic Markers

## Description

A geographic bubble map where markers are sized proportionally to quantitative data values at each location. Unlike scatter maps where size is optional, bubble maps use marker size as the primary visual encoding to show data magnitude across geographic regions. This visualization makes it immediately apparent where high and low values occur spatially, enabling intuitive comparison of quantities across locations.

## Applications

- Displaying city populations on a map with bubble size representing population magnitude
- Showing sales volume by store location with proportionally sized markers
- Visualizing earthquake magnitudes across a region with size indicating severity
- Mapping disease case counts by city or region with bubble size showing outbreak intensity

## Data

- `latitude` (numeric) - Geographic latitude coordinate (-90 to 90)
- `longitude` (numeric) - Geographic longitude coordinate (-180 to 180)
- `value` (numeric) - Quantitative variable for size encoding (e.g., population, sales, count)
- `label` (string, optional) - Location name or identifier for tooltips
- `category` (string, optional) - Categorical variable for color grouping
- Size: 15-150 points (fewer points than scatter maps to avoid excessive overlap)
- Example: World cities with population, regional sales data by location

## Notes

- Scale bubble area (not radius) proportionally to data values for accurate perception
- Use a size legend showing the relationship between bubble size and data values
- Apply transparency (alpha ~0.5-0.7) to handle overlapping bubbles in dense regions
- Include geographic context with country boundaries or coastlines as basemap
- Consider using a minimum bubble size to ensure small values remain visible
- For interactive libraries, enable hover tooltips showing exact values and location names
