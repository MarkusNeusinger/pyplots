# scatter-categorical: Categorical Scatter Plot

## Description

A scatter plot where points are colored according to a categorical variable. Each category has a distinct color, allowing visual comparison of patterns across groups. A legend maps colors to category names.

## Applications

- Visualizing relationships between variables across different groups
- Comparing correlation patterns by category
- Identifying clusters in multivariate data
- Exploratory analysis with group membership

## Data

The visualization requires:
- **X variable**: First continuous/numeric variable
- **Y variable**: Second continuous/numeric variable
- **Category variable**: Categorical grouping variable

Example structure:
```
X     | Y     | Category
------|-------|----------
1.2   | 3.4   | Group A
2.1   | 4.5   | Group B
1.8   | 3.9   | Group A
...
```

## Notes

- Use distinct, colorblind-safe colors for categories
- Include legend for category identification
- Marker shapes can also vary by group for additional distinction
- Consider alpha transparency for overlapping points
