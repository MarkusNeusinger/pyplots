# bar-grouped: Grouped Bar Chart

## Description

A grouped bar chart that displays multiple bars side-by-side for each category, enabling direct comparison of values across different groups within the same categorical dimension. This visualization excels at showing how different groups perform relative to each other across multiple categories, making patterns and differences immediately apparent. Grouped bar charts are essential for comparative analysis where you need to track multiple series against the same set of categories.

## Applications

- Comparing quarterly sales figures for multiple products across different regions
- Visualizing survey responses across demographic groups (age, gender, location)
- Displaying performance metrics for different teams or departments over several time periods

## Data

- `category` (categorical) - Labels for each group of bars on the x-axis
- `group` (categorical) - The different series being compared (creates side-by-side bars)
- `value` (numeric) - Heights of the bars representing the measured quantity
- Size: 3-8 categories with 2-5 groups recommended for readability
- Example: Monthly revenue by product line, test scores by subject across grade levels

## Notes

- Use distinct colors for each group with a clear legend
- Maintain consistent bar widths and spacing between groups
- Consider ordering categories or groups meaningfully (by value, alphabetically, or chronologically)
- Ensure adequate spacing between category groups for visual separation
- Value labels on bars are optional but helpful for precise comparisons
