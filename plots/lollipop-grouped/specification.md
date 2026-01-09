# lollipop-grouped: Grouped Lollipop Chart

## Description

A grouped lollipop chart displays multiple series across categorical variables using thin stems and circular markers arranged in groups. Each category has multiple lollipops side by side, one for each series, enabling direct comparison of metrics across groups. It combines the clarity of dot plots with the organization of grouped bar charts while reducing visual clutter.

## Applications

- Comparing sales performance across regions for multiple product lines
- Survey results showing scores for different questions across demographic groups
- Performance metrics (accuracy, speed, cost) across different algorithms or models
- Year-over-year comparisons of multiple KPIs across departments

## Data

- `category` (string) - Categorical labels for grouping (e.g., regions, departments)
- `series` (string) - Series identifier distinguishing each lollipop within a group
- `value` (numeric) - The measurement or count for each category-series combination
- Size: 3-8 categories with 2-5 series for optimal readability
- Example: Quarterly revenue by product line across 4 regions

## Notes

- Stems should be thin lines connecting baseline to marker
- Markers should be circular dots with distinct colors for each series
- Lollipops within a group should be positioned side by side with slight offset
- Include a legend to identify series colors
- Consider horizontal orientation if category labels are long
- Sort categories by a meaningful metric to reveal patterns
