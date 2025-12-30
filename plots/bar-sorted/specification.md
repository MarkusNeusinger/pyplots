# bar-sorted: Sorted Bar Chart

## Description

A sorted bar chart arranges bars in order of their values (typically descending from largest to smallest). This creates a clear visual hierarchy that makes it easy to identify the largest and smallest categories, see rankings, and understand relative magnitudes.

## Applications

- Ranking visualization (top 10 products, best performers)
- Pareto charts and 80/20 analysis
- Leaderboards and performance comparisons
- Frequency analysis (most common categories)
- Budget or resource allocation by department

## Data

The visualization requires:
- **Categorical variable**: Named categories
- **Numeric variable**: Values to sort and display

Example structure:
```
Category  | Value
----------|-------
Product A | 450
Product B | 280
Product C | 320
Product D | 190
...
```

## Notes

- Default sorting is descending (largest first)
- Horizontal orientation often works better for many categories or long labels
- Consider adding a cumulative line for Pareto analysis
- Color can highlight specific categories of interest
- Value labels on bars can improve readability
