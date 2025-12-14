# sankey-basic: Basic Sankey Diagram

## Description

A Sankey diagram visualizes flow or transfer between nodes using links with widths proportional to flow values. It excels at showing how quantities distribute from sources to destinations, revealing patterns in resource allocation, process flows, and system transitions. The diagram makes it easy to identify major pathways and compare relative magnitudes of different flows.

## Applications

- Visualizing energy flows from sources (coal, gas, nuclear) through transformation to end uses (heating, transport, industry)
- Tracking budget allocations from revenue sources through departments to specific expense categories
- Analyzing website traffic paths from entry pages through navigation to conversion or exit points

## Data

- `source` (categorical) - the origin node of each flow
- `target` (categorical) - the destination node of each flow
- `value` (numeric) - the magnitude of flow between source and target
- Size: 5-50 flows (too many flows reduce readability)
- Example: Energy flow data with sources like "Coal", "Gas", "Nuclear" flowing to sectors like "Residential", "Commercial", "Industrial"

## Notes

- Ensure no circular flows (source cannot equal target in the same link)
- Node labels should be clearly visible and not overlap with links
- Use distinct colors for different source categories or flow types
- Link opacity can help when flows cross over each other
