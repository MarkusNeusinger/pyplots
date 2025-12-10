# box-basic: Basic Box Plot

## Description

A box-and-whisker plot comparing statistical distributions across multiple groups. Each box displays quartiles (Q1, median, Q3), whiskers extend to show the data range within 1.5×IQR, and outliers appear as individual points. Excellent for comparing distributions and identifying outliers without assuming normality.

## Applications

- Comparing performance metrics across different teams or departments
- Analyzing price distributions across product categories
- Examining test scores across different classes or schools
- Visualizing response times across server regions

## Data

- `group` (categorical) - category labels for each box
- `value` (numeric) - values for distribution analysis
- Size: 3-8 groups, 30-100 values per group
- Example: performance data grouped by team or region
