# line-filled: Filled Line Plot

## Description

A line plot with the area between the line and the baseline (typically x-axis) filled with a semi-transparent color. This creates an area chart effect for a single series, emphasizing the magnitude of values.

## Applications

- Emphasizing magnitude of values over time
- Volume or quantity visualization
- Single series with area emphasis
- Stock price or metric trends

## Data

The visualization requires:
- **X variable**: Continuous variable (often time)
- **Y variable**: Single numeric variable

Example structure:
```
X    | Value
-----|-------
0    | 10
1    | 15
2    | 12
3    | 18
...
```

## Notes

- Fill should be semi-transparent (alpha ~0.3-0.5)
- Line should be visible on top of the fill
- Fill color typically matches line color
- Baseline is usually y=0
