# bar-stacked-labeled: Stacked Bar Chart with Total Labels

## Description

A stacked bar chart that displays multiple data series stacked on top of each other with total value labels prominently shown above each bar stack. This variant combines part-to-whole visualization with explicit numerical annotations, making it easy to read both individual segment contributions and cumulative totals at a glance. The total labels eliminate the need for mental arithmetic when comparing overall values across categories.

## Applications

- Comparing quarterly sales by product line with clear total revenue figures for executive presentations
- Displaying project budget breakdowns by task category with visible total costs for each project phase
- Visualizing survey response distributions with total respondent counts labeled for each question

## Data

- `category` (categorical) - Labels for each bar group on the x-axis (e.g., quarters, departments, regions)
- `component` (categorical) - The different series being stacked within each bar (e.g., product lines, cost types)
- `value` (numeric) - Size of each segment representing the measured quantity
- Size: 3-8 categories with 2-5 stacked components recommended for readability
- Example: Quarterly revenue by product category, department expenses by cost type

## Notes

- Total labels should be placed directly above each complete bar stack with clear formatting
- Use a consistent number format for labels (e.g., rounded integers, one decimal place, or with units)
- Ensure adequate vertical space above the tallest bar for label placement
- Consider using a slightly larger or bold font for total labels to distinguish from segment labels
- Segment labels within the bars are optional but can enhance readability for larger segments
