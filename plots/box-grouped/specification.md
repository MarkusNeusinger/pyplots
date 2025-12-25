# box-grouped: Grouped Box Plot

## Description

A grouped box plot displays multiple box plots side-by-side within each category, enabling comparison of distributions across subgroups. Each group contains boxes representing different subcategories or conditions, making it ideal for multi-factor comparisons and A/B testing scenarios with multiple metrics.

## Applications

- Comparing treatment effects across different patient demographics in clinical trials
- A/B testing with multiple metrics (conversion rate, time on site) across user segments
- Analyzing performance distributions by department and experience level
- Comparing experimental results across multiple factors in research studies

## Data

- `category` (string) - main group labels (x-axis categories)
- `subcategory` (string) - subgroup identifiers for side-by-side boxes
- `value` (numeric) - numerical values to plot
- Size: 20-200 points per subcategory, 2-6 categories, 2-4 subcategories

## Notes

- Display boxes side-by-side within each category with distinct colors
- Include a clear legend identifying each subcategory
- Maintain consistent box widths across all groups
- Show median line, quartile box, whiskers at 1.5*IQR, and outliers
