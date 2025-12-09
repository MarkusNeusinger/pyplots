# scatter-basic: Basic Scatter Plot

## Description

A fundamental scatter plot visualizing the relationship between two continuous variables. Each data point is represented as a marker at its (x, y) coordinate, making it ideal for identifying correlations, clusters, and outliers. Optimized for handling many data points with appropriate transparency.

## Applications

- Correlation analysis between height and weight in healthcare data
- Exploring relationship between advertising spend and sales revenue
- Identifying outliers in financial transaction data
- Visualizing the relationship between study hours and test scores

## Data

- `x` (numeric) - values for the horizontal axis
- `y` (numeric) - values for the vertical axis
- Size: 50-500 points
- Example: random correlated data or tips dataset (total_bill, tip)

## Notes

- Use alpha=0.7 for overlapping points
- Grid should be subtle (alpha=0.3)
