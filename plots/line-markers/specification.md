# line-markers: Line Plot with Markers

## Description

A line plot with visible markers at each data point, combining line and scatter plot features. This is particularly useful for sparse data where individual observations are significant.

## Applications

- Sparse datasets where each point matters
- Highlighting specific data points on trend lines
- Experimental data with discrete measurements
- Quality control charts with individual readings

## Data

The visualization requires:
- **X variable**: Continuous variable
- **One or more Y variables**: Series with data points to mark

Example structure:
```
X    | Value
-----|-------
0    | 10.5
1    | 12.3
2    | 11.8
3    | 14.2
...
```

## Notes

- Markers should be clearly visible against the line
- Use different marker shapes for multiple series
- Marker size should be proportional to line thickness
- Consider filled vs unfilled markers for distinction
