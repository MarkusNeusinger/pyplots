# network-transport-interactive: Interactive Transport Network Graph

## Description

An interactive multi-graph visualization for transportation networks where stations are displayed as rectangular nodes and trains/routes as directed edges connecting them. Edges are labeled with departure times, arrival times, and train identifiers, attaching to node handles distributed along the four sides of each rectangle. The visualization supports dragging nodes to reposition them while edges automatically adjust their paths. This is ideal for understanding complex timetables, connections, and routing patterns in rail or transit systems.

## Applications

- Analyzing train network timetables to identify connection opportunities and transfer points between services
- Visualizing public transit routes and schedules for operational planning and passenger information systems
- Mapping flight or bus connections between hubs to optimize scheduling and minimize layover times

## Data

- `stations` (list of dicts) - nodes with unique IDs, labels, and x/y coordinates for initial positioning
- `trains` (list of dicts) - directed edges with source station, target station, train ID, departure time, and arrival time
- `connections` (list of dicts, optional) - internal links within stations representing transfers between trains
- Size: 5-30 stations with 10-100 train connections for readable visualization
- Example: A regional rail network with 15 stations and 50 daily train services showing departure/arrival times

## Notes

- Stations should be rendered as rectangles with sufficient size to display labels and accommodate multiple edge handles
- Edge handles should be automatically distributed on the four sides of station rectangles based on edge direction and count
- Edges should display train ID and times as labels, with arrows indicating travel direction
- Implement drag-and-drop functionality for nodes with edges re-routing automatically
- Consider curved or orthogonal edge routing to avoid overlaps when multiple trains connect the same station pair
- Internal station connections (transfers) can be shown as links within the node or as small arcs
