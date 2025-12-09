# scatter-basic: Basic Scatter Plot

## Description

A fundamental scatter plot visualizing the relationship between two continuous variables. Each data point is represented as a marker at its (x, y) coordinate, making it ideal for identifying correlations, clusters, and outliers. Optimized for handling many data points with appropriate transparency.

## Data

**Required columns:**
- `x` (numeric) - values for the horizontal axis
- `y` (numeric) - values for the vertical axis

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 6, 7, 8],
    'y': [2.1, 4.3, 3.2, 5.8, 4.9, 7.2, 6.1, 8.5]
})
```

## Use Cases

- Correlation analysis between height and weight in healthcare data
- Exploring relationship between advertising spend and sales revenue
- Identifying outliers in financial transaction data
- Visualizing the relationship between study hours and test scores
