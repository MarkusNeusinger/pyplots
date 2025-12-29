# icicle-basic: Basic Icicle Chart

## Description

An icicle chart displaying hierarchical data as adjacent rectangles in a layered structure, where each rectangle's size represents its value in the hierarchy. Unlike treemaps that nest rectangles, icicle charts stack them in rows (horizontal) or columns (vertical), making parent-child relationships explicitly visible through spatial adjacency. This layout excels at showing both the hierarchy levels and the proportional values simultaneously.

## Applications

- File system visualization showing directory structure and file sizes
- Organizational hierarchy displaying departments and team headcounts
- Budget breakdown by department, project, and expense category
- Website navigation structure with page hierarchy and traffic volume

## Data

- `name` (string) - node label for each element in the hierarchy
- `parent` (string) - parent node reference establishing the tree structure
- `value` (numeric) - size/magnitude determining each rectangle's width or height
- Size: 10-100 nodes recommended
- Example: File system with nested folders and file sizes

## Notes

- Use horizontal orientation (top-to-bottom) for deep hierarchies
- Color by hierarchy level or category for visual grouping
- Label rectangles that have sufficient space; hide labels for small nodes
- Root node at top/left with children below/right
