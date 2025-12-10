# treemap-basic: Treemap Chart

## Description

A treemap displays hierarchical data as nested rectangles, where the area of each rectangle represents a quantitative value such as size, count, or amount. The nested structure reveals parent-child relationships while the visual area encoding makes it easy to compare values across the hierarchy. This visualization excels at showing part-to-whole relationships and identifying dominant elements within complex hierarchical structures.

## Applications

- Visualizing disk space usage by folder and subfolder to identify storage-heavy directories
- Displaying portfolio allocation by sector and individual stock holdings
- Analyzing budget breakdown by department and expense category

## Data

- `id` (string) - Unique identifier for each rectangle
- `parent` (string) - Parent rectangle identifier (empty for root)
- `label` (string) - Display label for the rectangle
- `value` (numeric) - Size value determining rectangle area
- Size: 20-200 rectangles across 2-4 hierarchy levels
- Example: Company budget with departments, teams, and expense types

## Notes

- Use squarified treemap algorithm for optimal aspect ratios when available
- Color coding should distinguish top-level categories or encode a secondary value
- Labels should be readable, hidden or truncated for small rectangles
- Interactive libraries should support hover tooltips showing value and percentage
- Border styling should clearly delineate hierarchy levels
