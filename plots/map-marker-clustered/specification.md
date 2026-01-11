# map-marker-clustered: Clustered Marker Map

## Description

A geographic map that dynamically clusters nearby markers based on the current zoom level. At lower zoom levels, clusters aggregate multiple points into a single marker displaying the count, while zooming in progressively expands clusters to reveal individual markers. This visualization is essential for efficiently displaying large geographic datasets without visual clutter, enabling users to see both the overall distribution and specific locations through interactive exploration.

## Applications

- Store locator maps showing retail locations that cluster regionally and expand to individual stores when zoomed
- Event venue mapping where concerts, conferences, or festivals are grouped by city or neighborhood
- POI (Point of Interest) visualization for tourism, real estate, or service directories
- Large-scale geographic datasets (e.g., sensor networks, incident reports) where thousands of points need efficient display

## Data

- `lat` (numeric) - Latitude coordinate of each point (-90 to 90)
- `lon` (numeric) - Longitude coordinate of each point (-180 to 180)
- `label` (string, optional) - Display label for individual markers when expanded
- `category` (string, optional) - Category for color-coding markers and clusters
- Size: 100-5000 points (clustering enables effective display of large datasets)
- Example: Store locations with name and type, event venues with event name and category

## Notes

- Cluster markers should display the count of grouped points
- Implement smooth zoom transitions when clusters expand or collapse
- Use distinct colors for different categories, with cluster markers reflecting the dominant or mixed category
- Enable click-to-zoom behavior on clusters to expand and reveal contents
- Consider showing a convex hull or spider lines when hovering over clusters to indicate member locations
- Include a basemap with appropriate geographic context (boundaries, streets, or terrain)
