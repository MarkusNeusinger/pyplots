# map-connection-lines: Connection Lines Map (Origin-Destination)

## Description

A geographic map visualization showing connection lines (arcs or great circles) between pairs of locations. This plot excels at revealing spatial patterns in flows, routes, and relationships between places. The curved lines naturally represent shortest paths on Earth's surface while avoiding visual overlap with straight lines. Line properties like thickness or color can encode additional variables such as traffic volume or connection type.

## Applications

- Visualizing airline flight routes between airports showing connection frequency or passenger volume
- Mapping migration flows between countries or regions with line weight indicating population movement
- Displaying trade routes and shipping connections between ports with intensity showing trade volume
- Showing network infrastructure connections between data centers or communication nodes

## Data

- `origin_lat` (numeric) - Latitude of the starting point (-90 to 90)
- `origin_lon` (numeric) - Longitude of the starting point (-180 to 180)
- `dest_lat` (numeric) - Latitude of the destination point (-90 to 90)
- `dest_lon` (numeric) - Longitude of the destination point (-180 to 180)
- `value` (numeric, optional) - Connection weight for line thickness or color intensity
- `label` (string, optional) - Route name or identifier for tooltips
- Size: 10-100 connections (too many connections reduce readability)
- Example: Flight routes between major airports with passenger counts

## Notes

- Use curved lines (great circle arcs) for long-distance connections to represent geodesic paths
- Line thickness or color intensity should represent the value/weight when provided
- Include location markers (points) at origin and destination endpoints
- Apply transparency (alpha ~0.3-0.6) to handle overlapping routes
- Show a base map with country borders or coastlines for geographic context
- Consider using a global projection (Robinson, Natural Earth) for world maps
