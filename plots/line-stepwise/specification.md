# line-stepwise: Step Line Plot

## Description

A step function plot where values remain constant until the next change, creating horizontal-then-vertical transitions. This visualization emphasizes discrete changes rather than interpolated values.

## Applications

- Discrete state changes over time
- Price/value stepping (stock prices at close)
- Cumulative counts that increase discretely
- Digital signals and binary states
- Piecewise constant functions

## Data

The visualization requires:
- **X variable**: Continuous or discrete variable (often time)
- **Y variable**: Values that change at specific points

Example structure:
```
X    | Value
-----|-------
0    | 100
1    | 100
2    | 150
3    | 150
4    | 125
...
```

## Notes

- Step alignment options: 'pre' (before), 'mid' (middle), 'post' (after)
- Clear distinction from smooth line interpolation
- Horizontal segments show value persistence
- Vertical segments show instantaneous changes
