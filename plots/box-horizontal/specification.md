# box-horizontal: Horizontal Box Plot

## Description

A horizontal box plot displays the distribution of numerical data through quartiles with the boxes oriented horizontally. This orientation is particularly useful when category labels are long or when comparing many groups, as it allows for easier reading of labels on the y-axis.

## Applications

- Comparing distributions across many categories with long names
- Displaying salary ranges by job title or department
- Analyzing test score distributions by course or subject
- Visualizing response time distributions by service type

## Data

The visualization requires:
- **Categorical variable**: Groups or categories (displayed on y-axis)
- **Numeric variable**: Values to show distribution (displayed on x-axis)

Example structure:
```
Category    | Value
------------|-------
Category A  | 45.2
Category A  | 52.1
Category B  | 38.7
Category B  | 41.3
...
```

## Notes

- Same statistical elements as vertical box plot: median line, quartile box, whiskers, outliers
- Particularly effective when category names are long
- Consider sorting categories by median value for easier comparison
- Whiskers typically extend to 1.5 * IQR
