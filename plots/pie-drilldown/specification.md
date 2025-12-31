# pie-drilldown: Drilldown Pie Chart with Click Navigation

## Description

A pie chart with hierarchical drilldown functionality that displays one level of data at a time. Clicking on any slice reveals a detailed breakdown of that category's subcategories as a new pie chart. Breadcrumb navigation allows users to traverse back up the hierarchy. This interactive visualization is ideal for exploring multi-level categorical data without the visual complexity of showing all levels simultaneously.

## Applications

- Sales data exploration by region, then country, then city
- Budget breakdown from department to team to individual expense categories
- Website analytics drilling from traffic source to campaign to keyword
- Product category navigation from main category to subcategory to product line

## Data

- `id` (string) - unique identifier for each node
- `name` (string) - display label for the category
- `value` (numeric) - value for leaf nodes (determines slice size)
- `parent` (string) - id of parent node (null/empty for root level)
- Size: 3-8 categories per level, 2-4 hierarchy levels
- Structure: hierarchical/tree with parent-child relationships

## Notes

- Show breadcrumb trail at top (e.g., "All > Electronics > Phones")
- Include a "back" button or clickable breadcrumbs to navigate up
- Animate transitions when drilling down or up
- Display percentage and value labels on slices
- Use consistent color schemes within branches when possible
- Show a visual indicator (icon or cursor change) that slices are clickable
