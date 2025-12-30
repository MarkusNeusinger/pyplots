# cat-strip: Categorical Strip Plot

## Description

A categorical scatter plot that displays individual data points for each category along one axis, with random horizontal jitter applied to reduce overlapping points. Shows the distribution of values within each group.

## Applications

- Comparing distributions across categories
- Visualizing individual observations
- Identifying outliers within groups
- Small to medium dataset exploration

## Data

The visualization requires:
- **Categorical variable**: Groups/categories on one axis
- **Numeric variable**: Values on the other axis

Example structure:
```
Category | Value
---------|-------
A        | 23.5
A        | 25.1
B        | 18.2
B        | 19.8
...
```

## Notes

- Jitter prevents point overlap
- Best for smaller datasets where individual points are visible
- Can be combined with other plot types (box, violin)
- Points can be colored by additional variable
