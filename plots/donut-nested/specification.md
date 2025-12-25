# donut-nested: Nested Donut Chart

## Description

A nested donut chart displays hierarchical data as multiple concentric rings, where each ring represents a level of the hierarchy. Inner rings show parent categories while outer rings show their subdivisions. This visualization effectively reveals part-to-whole relationships across multiple levels while maintaining the familiar donut format.

## Applications

- Budget allocation showing department totals (inner) and expense categories (outer)
- Market share by region (inner) and product lines within each region (outer)
- Organization structure showing divisions and their teams
- Revenue breakdown by business unit and customer segments

## Data

- `level_1` (string) - parent category labels (inner ring)
- `level_2` (string) - child category labels (outer ring)
- `value` (numeric) - values for the innermost level
- Size: 3-6 parent categories, 2-5 children each
- Hierarchy: values aggregate from outer rings to inner rings

## Notes

- Use consistent color families per parent category (same hue, varying lightness)
- Align child segments with parent segment boundaries for clarity
- Include labels on larger segments, use legend for smaller ones
- Consider adding spacing between rings for visual separation
- Limit to 2-3 hierarchy levels to maintain readability
