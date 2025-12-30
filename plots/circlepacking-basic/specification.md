# circlepacking-basic: Circle Packing Chart

## Description

A circle packing chart displays hierarchical data as nested circles, where each circle contains smaller circles representing its children. Circle size is proportional to node value, and circles are packed efficiently without overlap. This visualization excels at revealing hierarchical structures while simultaneously showing quantitative relationships through area encoding.

## Applications

- File and folder size visualization showing directory hierarchy and storage consumption
- Organizational structure display with team sizes proportional to headcount or budget
- Portfolio composition analysis breaking down investments by asset class and holdings
- Taxonomy or classification hierarchies with proportional representation of categories

## Data

- `id` (string) - unique identifier for each node
- `parent` (string) - parent node identifier (null for root)
- `value` (numeric) - size value determining circle area (for leaf nodes)
- `label` (string) - display name for the node
- Size: 20-200 nodes across 2-4 hierarchy levels

## Notes

- Pack circles efficiently using force simulation or specialized packing algorithms
- Color by depth level or category to distinguish hierarchy levels
- Display labels for larger circles; smaller circles may show labels on hover
- Scale circle sizes by area (not radius) for accurate visual perception
- Root circle should encompass all children with appropriate padding
