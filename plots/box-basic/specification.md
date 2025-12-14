# box-basic: Basic Box Plot

## Description

A box plot (box-and-whisker plot) showing the distribution of numerical data through quartiles. Displays the median, first and third quartiles as a box, with whiskers extending to show the data range. Essential for comparing distributions across categories and identifying outliers.

## Applications

- Comparing salary distributions across departments
- Analyzing test score distributions by class
- Quality control: comparing measurements across production batches
- Research: comparing experimental groups

## Data

- `category` (string) - group labels for comparison
- `value` (numeric) - numerical values to plot
- Size: 20-500 points per category, 2-8 categories

## Notes

- Show median line within the box
- Display outliers as individual points
- Include whiskers at 1.5*IQR
- Use different colors for each category
