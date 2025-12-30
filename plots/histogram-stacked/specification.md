# histogram-stacked: Stacked Histogram

## Description

A histogram showing multiple groups stacked on top of each other within each bin. The total bar height represents the combined frequency, while colored segments show individual group contributions.

## Applications

- Comparing distributions of multiple groups
- Showing composition within histogram bins
- Total frequency with group breakdown
- Demographic or categorical comparisons

## Data

The visualization requires:
- **Continuous variable**: Values to bin
- **Category variable**: Group membership for stacking

Example structure:
```
Value | Group
------|-------
12.5  | A
18.3  | B
15.7  | A
22.1  | B
14.2  | C
...
```

## Notes

- Same bin boundaries applied to all groups
- Distinct colors for each group
- Legend shows group labels
- Total bar height = combined frequency
- Consider ordering groups by size within bins
