# histogram-cumulative: Cumulative Histogram

## Description

A cumulative histogram (also known as an ogive or cumulative frequency histogram) displays the running total of observations up to each bin boundary. The y-axis shows cumulative count or proportion, creating a monotonically increasing step function that reaches the total sample size (or 1.0 for normalized).

## Applications

- Visualizing percentiles and quantile positions
- Understanding data distribution thresholds (e.g., "what percentage is below X?")
- Quality control and process analysis
- Comparing empirical vs theoretical CDFs
- Financial risk analysis (Value at Risk)

## Data

The visualization requires:
- **Numeric variable**: Continuous values to bin and accumulate

Example structure:
```
Value
------
12.5
18.3
15.7
22.1
...
```

## Notes

- Y-axis shows cumulative count or proportion (0 to n, or 0 to 1)
- The curve is always monotonically non-decreasing
- Often displayed as steps (not smooth curves) to show discrete bins
- Can use `density=True` or `cumulative=True` parameters
- Useful for determining what proportion of data falls below any threshold
