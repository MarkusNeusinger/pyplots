# bar-drilldown: Column Chart with Hierarchical Drilling

## Description

A column/bar chart with hierarchical drilldown functionality that displays one level of categorical data at a time. Clicking on any column reveals a detailed breakdown of that category's subcategories as a new bar chart at the next level. Breadcrumb navigation allows users to traverse back up the hierarchy. This interactive visualization excels at exploring multi-level categorical data while maintaining precise value comparisons that bar charts provide.

## Applications

- Time-based drill navigation (year to quarter to month)
- Geographic data exploration (region to country to city)
- Product hierarchy exploration (category to subcategory to product)
- Financial statement breakdown (department to team to expense type)

## Data

- `id` (string) - unique identifier for each node
- `name` (string) - display label for the category
- `value` (numeric) - data value determining column height
- `parent` (string) - id of parent node (null/empty for root level)
- Size: 3-8 categories per level, 2-3 hierarchy levels deep
- Structure: hierarchical/tree with parent-child relationships

## Notes

- Click on a column to drill into its sub-level breakdown
- Display breadcrumb trail for navigation (e.g., "All > Region > Country")
- Provide a back button or clickable breadcrumbs to drill up
- Animate transitions between hierarchy levels for smooth UX
- Maintain consistent color mapping across drill levels when possible
- Show visual indicator (cursor change or icon) that columns are clickable
- Display value labels on columns for precise comparison
