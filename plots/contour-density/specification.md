# contour-density: Density Contour Plot

## Description

A density contour plot (also known as a 2D KDE contour plot) displays the concentration of points in a 2D scatter plot using contour lines. The contours connect points of equal density, revealing clusters, patterns, and the overall bivariate distribution shape.

## Applications

- Visualizing bivariate distributions
- Finding clusters and patterns in large scatter datasets
- Geographic point concentration analysis
- Quality control (identifying process clusters)
- Scientific data where density matters more than individual points

## Data

The visualization requires:
- **X variable**: First continuous variable
- **Y variable**: Second continuous variable

Example structure:
```
X     | Y
------|------
1.2   | 3.4
2.1   | 4.5
1.8   | 3.9
...
```

## Notes

- Alternative to scatter plot for very large datasets (avoids overplotting)
- Kernel density estimation (KDE) is used to compute density
- Multiple contour levels show density gradients (inner = higher density)
- Can be combined with scatter plot overlay for context
- Filled contours (contourf) can also be used for stronger visual impact
- Consider bandwidth/smoothing parameter for optimal results
