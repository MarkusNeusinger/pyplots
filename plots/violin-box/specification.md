# violin-box: Violin Plot with Embedded Box Plot

## Description

A violin plot with an embedded box plot inside, combining the distribution shape visualization (KDE) with traditional quartile statistics. Shows both the probability density and summary statistics in one plot.

## Applications

- Complete distribution visualization
- Combining density estimate with summary statistics
- Detailed group comparisons
- Statistical presentations requiring both views

## Data

The visualization requires:
- **Numeric variable**: Values to show distribution
- **Categorical variable**: Groups to compare

Example structure:
```
Value | Group
------|-------
45.2  | A
52.1  | A
38.7  | B
41.3  | B
...
```

## Notes

- Box plot centered inside violin
- Shows median, quartiles (box), and whiskers
- KDE (violin) shape visible around the box
- Outliers can be shown as points
