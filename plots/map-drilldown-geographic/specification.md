# map-drilldown-geographic: Drillable Geographic Map

## Description

A hierarchical map with drill-down capability that navigates from country to state/province to city level, revealing progressively more geographic detail on click. Each region is colored according to a data value (choropleth style), and clicking a region zooms into its subdivisions with aggregated values. Breadcrumb navigation allows users to traverse back up the hierarchy. This visualization excels at exploring multi-level administrative data where users need both the big picture and granular detail.

## Applications

- Analyzing sales performance by region, drilling from country to state to city to identify top-performing areas
- Exploring population statistics at multiple administrative levels for demographic research
- Visualizing election results or survey responses with the ability to drill into specific regions
- Navigating hierarchical geographic reporting dashboards for business intelligence

## Data

- `country` (string) - Country name or ISO code (top level)
- `state` (string) - State or province name (second level)
- `city` (string, optional) - City name (third level, leaf nodes)
- `value` (numeric) - Data value at each level (e.g., sales, population, percentage)
- Size: 5-50 countries at top level, 5-30 states per country, 5-20 cities per state
- Structure: Hierarchical with parent-child relationships implied by geographic containment

## Notes

- Click any region to drill down to the next administrative level
- Display breadcrumb navigation (e.g., "World > United States > California") with clickable segments to navigate back up
- Smooth zoom transitions when drilling down or up to maintain spatial context
- Parent-level values should aggregate child values (sum, average, or weighted average as appropriate)
- Use a consistent color scale across all levels to enable meaningful comparison
- Show a color legend indicating the value range
- For interactive libraries, include tooltips showing region name and value on hover
- Handle regions with no sub-level data gracefully (show as non-clickable or with visual indicator)
