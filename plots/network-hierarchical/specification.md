# network-hierarchical: Hierarchical Network Graph with Tree Layout

## Description

A hierarchical network graph organizes nodes in distinct levels from root to leaves, with edges showing parent-child relationships between levels. Unlike force-directed layouts that optimize for aesthetic spacing, hierarchical layouts explicitly encode tree structure by positioning nodes at fixed vertical or horizontal levels. This visualization reveals organizational depth, branching patterns, and the overall tree structure at a glance.

## Applications

- Visualizing organizational charts showing reporting relationships from executives to individual contributors
- Displaying file system or directory structures with folders and subfolders organized by depth
- Mapping software class hierarchies showing inheritance relationships from base to derived classes
- Illustrating decision trees or classification hierarchies with clear branching paths

## Data

- `nodes` (list of dicts) - entities with unique IDs, labels, and optional level or parent attributes
- `edges` (list of tuples) - parent-child connections as (parent_id, child_id) pairs
- `level` (integer, optional) - explicit level assignment for each node (0 = root)
- Size: 10-50 nodes for readable static visualization
- Example: A small organizational chart with 30 employees across 4 management levels

## Notes

- Use tree or hierarchical layout algorithms (e.g., NetworkX's graphviz_layout with 'dot')
- Root nodes should be positioned at the top (or left for horizontal layouts)
- Edges should be straight or curved lines without arrows unless direction needs emphasis
- Consider edge bundling for trees with many nodes to reduce visual clutter
- Node spacing should be proportional to prevent overlap at crowded levels
