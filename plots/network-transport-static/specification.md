# network-transport-static: Static Transport Network Diagram

## Description

A directed network visualization for transportation systems where stations are displayed as labeled nodes and train/bus routes as directed edges. Edges display departure times, arrival times, and route identifiers. Designed for visualizing timetables, route maps, and connection patterns in rail, bus, or flight networks. This static version focuses on clear, readable presentation without interactive repositioning.

## Applications

- Visualizing regional train networks with departure and arrival times at each station
- Displaying bus route maps showing service frequency and travel times between stops
- Analyzing flight connections between airports with layover and connection information
- Planning public transit coverage by mapping routes and identifying service gaps

## Data

- `stations` (list of dicts) - nodes with `id`, `label`, `x`, `y` coordinates for positioning
- `routes` (list of dicts) - directed edges with `source_id`, `target_id`, `route_id`, `departure_time`, `arrival_time`
- Size: 8-20 stations with 15-60 routes for optimal readability
- Example: A regional rail network with 12 stations and 35 daily train services showing hourly departures

## Notes

- Station nodes should display labels clearly; size nodes to accommodate station names
- Edges must show direction with arrows indicating travel direction
- Edge labels should display route identifier and times (e.g., "RE 42 | 08:15 → 09:30")
- When multiple routes connect the same station pair, use curved or offset edges to distinguish them
- Node positioning based on provided x/y coordinates; no force-directed layout needed
- Consider color-coding routes by type (regional, express, local) or frequency
- Tooltips (where supported) should show full route details on hover
