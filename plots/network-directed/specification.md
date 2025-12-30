# network-directed: Directed Network Graph

## Description

A directed network graph visualizes relationships between entities using nodes connected by edges with arrows, indicating the direction of relationships or flow. Unlike undirected graphs, directed graphs reveal asymmetric relationships such as dependencies, hierarchies, or information flow. The arrows clearly communicate which entity points to which, making cause-and-effect relationships and directional dependencies immediately visible.

## Applications

- Mapping software module dependencies to understand build order and identify circular dependencies
- Visualizing citation networks where arrows show which papers cite which others
- Displaying organizational reporting structures or workflow approval chains
- Analyzing web page link structures to understand navigation patterns and page authority

## Data

- `nodes` (list of dicts) - entities with unique IDs and optional attributes like label or group
- `edges` (list of tuples/dicts) - directed connections as (source_id, target_id) pairs where arrows point from source to target
- `weight` (numeric, optional) - edge weight that can affect arrow thickness or style
- Size: 10-50 nodes for clear static visualization (larger networks require interactive exploration)
- Example: Software package dependencies where arrows show import direction

## Notes

- Arrows should be clearly visible and appropriately sized relative to node size
- Consider curved edges when nodes have bidirectional connections to avoid arrow overlap
- Node position can use force-directed layout, hierarchical layout, or circular layout depending on data structure
- Arrow style (filled, open, curved) should be consistent throughout the graph
