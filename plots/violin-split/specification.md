# violin-split: Split Violin Plot

## Description

A split violin plot displaying two distributions side-by-side within each violin, with each half representing a different group. Unlike standard violin plots that mirror the same distribution, split violins use the left and right halves to compare two conditions (such as before/after, male/female, or control/treatment) at each category level. This enables direct visual comparison of distribution shapes between paired groups.

## Applications

- Comparing patient outcomes before and after treatment across multiple clinics
- Analyzing salary distributions by gender across job categories
- Comparing test score distributions between control and experimental groups
- Visualizing seasonal patterns (summer vs winter) across different regions

## Data

- `category` (string) - group labels for the x-axis (e.g., department, region)
- `value` (numeric) - numerical values to plot as distributions
- `split_group` (string/binary) - binary grouping variable for left/right halves
- Size: 30-500 points per category per split group, 2-6 categories

## Notes

- Use distinct colors for each split group with legend
- Ensure the two halves meet at the center line
- Consider adding inner box plot or quartile markers
- Alpha transparency helps when distributions overlap at center
