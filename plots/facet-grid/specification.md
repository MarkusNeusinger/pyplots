# facet-grid: Faceted Grid Plot

## Description

A grid of subplots where each cell shows the same type of plot for a different subset of data, split by one or two categorical variables. Enables systematic comparison across multiple dimensions.

## Applications

- Multi-dimensional data exploration
- Comparing patterns across categories
- Conditional distribution analysis
- Publication-ready multi-panel figures

## Data

The visualization requires:
- **Numeric variables**: For the base plot (x, y)
- **Faceting variable(s)**: Categorical variables to split by (row, column)

Example structure:
```
X    | Y    | Row_Var | Col_Var
-----|------|---------|--------
1.2  | 3.4  | A       | X
2.3  | 4.5  | A       | Y
3.1  | 2.8  | B       | X
...
```

## Notes

- All subplots share the same axes scales by default
- Can facet by row, column, or both
- Base plot can be scatter, line, histogram, etc.
- Labels identify each facet's category
