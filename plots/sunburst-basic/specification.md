# sunburst-basic: Sunburst Chart

## Description

A sunburst chart displays hierarchical data as concentric rings radiating outward from a central point, where each ring represents a level in the hierarchy. The angular width of each segment shows its proportion relative to its parent, making it effective for visualizing part-to-whole relationships across multiple hierarchy levels. This visualization excels at revealing both the structure and relative sizes within nested categorical data.

## Applications

- Visualizing file system disk usage showing folder sizes across directory levels
- Displaying organizational structure with headcount or budget allocation per department and team
- Analyzing product sales breakdown by category, subcategory, and individual items

## Data

- `id` (string) - Unique identifier for each segment
- `parent` (string) - Parent segment identifier (empty for root)
- `label` (string) - Display label for the segment
- `value` (numeric) - Size value determining segment angle
- Size: 20-200 segments across 2-5 hierarchy levels
- Example: Organizational budget with departments, teams, and projects

## Notes

- Root node should be centered with child segments radiating outward
- Color coding should distinguish top-level categories or hierarchy levels
- Segment labels should be readable, hidden for small segments if needed
- Interactive libraries should support hover tooltips showing value and percentage
