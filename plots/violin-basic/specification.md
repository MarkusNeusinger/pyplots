# violin-basic: Basic Violin Plot

## Description

A violin plot combining a box plot with a kernel density estimation on each side, showing the distribution shape of numerical data. The width of the violin at each point represents the frequency of data values at that level. Excellent for comparing distributions across categories while revealing their underlying shape, providing more detail than a traditional box plot.

## Applications

- Comparing salary distributions across job titles
- Analyzing test score distributions by school
- Comparing customer spending patterns by segment
- Research: comparing measurement distributions between groups

## Data

- `category` (string) - group labels for comparison
- `value` (numeric) - numerical values to plot
- Size: 30-1000 points per category, 2-6 categories

## Notes

- Show quartile markers inside the violin
- Use mirrored density on both sides
- Include median line
- Consider split violins for comparing two conditions
