# lollipop-basic: Basic Lollipop Chart

## Description

A lollipop chart displays categorical data with thin lines (stems) extending from a baseline to circular markers (dots) at each data point. It presents the same information as a bar chart but with a cleaner, more minimalist aesthetic that reduces visual clutter while maintaining clear value comparisons.

## Applications

- Ranking top performers across categories (e.g., sales by region, employee scores)
- Survey results with many response categories where bars would look cluttered
- Year-over-year or period comparisons with discrete categories
- Displaying sorted metrics where the relative position and exact value both matter

## Data

- `category` (string) - Categorical labels for each data point
- `value` (numeric) - The measurement or count for each category
- Size: 5-20 categories for optimal readability
- Example: Product sales by category, sorted by value

## Notes

- Stems should be thin lines connecting baseline to marker
- Markers should be circular dots clearly visible at data values
- Vertical orientation preferred (categories on x-axis, values on y-axis)
- Data sorted by value improves readability
- Consider horizontal orientation if category labels are long
