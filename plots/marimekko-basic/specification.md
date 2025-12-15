# marimekko-basic: Basic Marimekko Chart

## Description

A Marimekko chart (also called mekko or mosaic plot) is a stacked bar chart where both the width and height of segments represent data values. This visualization shows two categorical dimensions simultaneously with proportional areas, making it ideal for understanding how parts relate to wholes across categories of different sizes.

## Applications

- Market share analysis across segments of varying market sizes
- Product mix visualization by customer segment or region
- Revenue breakdown by region and product line
- Cross-tabulation data where both dimensions matter equally

## Data

- `x_category` (categorical) - Categories determining bar widths (e.g., market segments, regions)
- `y_category` (categorical) - Categories within each bar for stacking (e.g., products, brands)
- `value` (numeric) - Values determining segment sizes; bar width proportional to column total, segment height proportional to share within column
- Size: 3-7 x-categories, 2-5 y-categories typical for readability
- Example: Market share data with regions as x-categories and product lines as y-categories

## Notes

- Bar widths should be proportional to the total value of each x-category
- Segment heights within each bar show the proportion of each y-category
- Area of each segment represents the actual value (width x height proportion)
- Color coding should distinguish y-categories clearly with a legend
- Consider adding value labels on larger segments for readability
- X-axis can show category names centered under each variable-width bar
