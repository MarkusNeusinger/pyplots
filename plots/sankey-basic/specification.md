# sankey-basic: Basic Sankey Diagram

## Description

A Sankey diagram visualizes flows and transfers between categories, with the width of each connecting band proportional to the quantity of flow. It is ideal for showing how resources, energy, or values are distributed from one set of categories to another. Sankey diagrams reveal major pathways and help identify bottlenecks or dominant flows in a system.

## Applications

- Visualizing energy flows from sources through conversion to end uses in sustainability reports
- Tracking website user journeys from landing pages through navigation to conversions
- Displaying budget allocations from revenue sources to department expenditures

## Data

- `source` (categorical) - the origin node/category of the flow
- `target` (categorical) - the destination node/category of the flow
- `value` (numeric) - the magnitude or quantity of the flow
- Size: 5-50 flows between 3-15 unique nodes
- Example: energy consumption by sector, budget distribution, customer journey paths

## Notes

- Node order and positioning should minimize link crossings for readability
- Use distinct colors for source nodes or flow categories
- Consider adding labels showing flow values on major connections
