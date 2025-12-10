# violin-basic: Basic Violin Plot

## Description

A violin plot showing the distribution shape of multiple categories using mirrored kernel density estimation curves. Combines the density visualization of KDE plots with the statistical markers of box plots, making it ideal for comparing distributions across groups while revealing their full shape including multimodality, skewness, and density variations.

## Applications

- Comparing salary distributions across departments to identify compensation patterns and outliers
- Analyzing response time distributions across different API endpoints to spot performance issues
- Visualizing test score distributions across different teaching methods to evaluate effectiveness
- Examining product rating distributions across categories to understand customer satisfaction patterns

## Data

- `category` (categorical) - group labels for side-by-side comparison (3-6 groups recommended)
- `value` (numeric, continuous) - the variable whose distribution is visualized
- Size: 50-500 observations per category for smooth density estimation
- Example: Employee performance scores grouped by department

## Notes

- Use inner box plot markers (median line, quartile box) to show summary statistics
- Mirrored density curves should be symmetric and smoothly rendered via KDE
- Bandwidth selection affects smoothness - use library defaults or Scott's rule
- Consider horizontal orientation for long category labels
- Width should be normalized so all violins have comparable maximum widths
