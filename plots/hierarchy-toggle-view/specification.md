# hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View

## Description

An interactive hierarchical visualization that allows users to toggle between treemap and sunburst representations of the same data. The treemap displays hierarchy as nested rectangles with area proportional to values, while the sunburst shows the same structure as concentric radial segments. This dual-view approach enables users to explore hierarchical data from different perspectives: rectangular layouts excel at precise size comparison, while radial layouts better reveal hierarchical depth and parent-child relationships.

## Applications

- File system explorers allowing users to switch between space-efficient treemap and relationship-focused sunburst views
- Budget visualization dashboards where analysts toggle views to compare allocations (treemap) vs drill down hierarchy (sunburst)
- Organizational structure tools that switch between compact department overview and radial reporting chain visualization
- Portfolio analysis platforms toggling between market cap comparison and sector hierarchy exploration

## Data

- `id` (string) - unique identifier for each node
- `parent` (string) - parent node id (null/empty for root)
- `label` (string) - display name for the node
- `value` (numeric) - size/magnitude determining area (treemap) or angle (sunburst)
- Size: 15-60 nodes across 2-4 hierarchy levels

## Notes

- Implement a clear toggle button or switch control to change between views
- Maintain consistent colors across both views so nodes are easily identifiable
- Preserve selection/hover state when switching between views if possible
- Smooth animated transitions between layouts enhance user experience
- Both views should fit within the same container dimensions
