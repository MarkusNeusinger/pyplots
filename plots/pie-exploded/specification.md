# pie-exploded: Exploded Pie Chart

## Description

A pie chart with one or more slices visually separated (exploded) from the center to emphasize specific segments. The explosion effect draws viewer attention to key data points while maintaining the overall proportional relationships. Ideal for highlighting important categories, outliers, or segments that require special attention in presentations and reports.

## Applications

- Highlighting the market leader in competitive analysis
- Emphasizing budget overruns in a single department
- Drawing attention to the largest customer segment
- Showcasing outlier categories in survey results

## Data

- `category` (string) - category labels for each slice
- `value` (numeric) - values determining slice proportions
- `explode` (numeric) - explosion distance for each slice (0 = no explosion, 0.1 = typical)
- Size: 3-8 categories (optimal for readability)

## Notes

- Explosion distance should be controllable per slice
- Include percentage labels on slices
- Use distinct colors for each category
- Typically explode 1-3 slices maximum to maintain visual clarity
- Add a legend for category identification
