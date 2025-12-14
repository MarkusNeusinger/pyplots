# sunburst-basic: Basic Sunburst Chart

## Description

A sunburst chart displays hierarchical data as concentric rings, where each ring represents a level in the hierarchy. Inner rings show parent categories while outer rings show their children, with segment angles proportional to values. This radial visualization excels at revealing hierarchical structures and part-to-whole relationships across multiple levels simultaneously.

## Applications

- File system visualization showing directory sizes and nested folder structures
- Organizational budget breakdown by department, team, and project
- Taxonomy or classification hierarchies with proportional representation
- Website navigation paths showing user flow through page hierarchies

## Data

- `level_1` (string) - root/parent category (innermost ring)
- `level_2` (string) - child category (second ring)
- `level_3` (string) - optional grandchild category (outer ring)
- `value` (numeric) - size/magnitude determining segment angle
- Size: 10-50 leaf nodes across 2-4 hierarchy levels

## Notes

- Use consistent colors within each branch to show relationships
- Label major segments; smaller segments may show labels on hover/interaction
- Maintain clear visual separation between hierarchy levels
- Inner segments should visually encompass their children's angular span
