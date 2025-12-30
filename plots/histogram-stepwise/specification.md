# histogram-stepwise: Step Histogram

## Description

A histogram displayed as step lines (outline only) without filled bars. The distribution is shown as connected horizontal and vertical line segments, creating a step function appearance.

## Applications

- Comparing multiple distributions without visual overlap
- Clean, minimal histogram visualization
- Overlaying distributions for direct comparison
- Print-friendly histogram representation

## Data

The visualization requires:
- **Continuous variable**: Values to bin and count

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

- No fill, only outline (step lines)
- Each bin represented by horizontal segment at count level
- Vertical segments connect adjacent bins
- Ideal for overlaying multiple distributions
