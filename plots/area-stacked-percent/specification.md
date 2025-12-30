# area-stacked-percent: 100% Stacked Area Chart

## Description

A stacked area chart normalized to 100%, where each area represents the percentage contribution of a category to the total. The combined height always equals 100%, showing proportional changes over time.

## Applications

- Market share evolution over time
- Portfolio composition changes
- Budget allocation trends
- Demographic proportion shifts

## Data

The visualization requires:
- **X variable**: Continuous variable (typically time)
- **Multiple Y variables**: Categories to stack (values normalized to percentages)

Example structure:
```
Time | Category A | Category B | Category C
-----|------------|------------|------------
2020 | 40         | 35         | 25
2021 | 45         | 30         | 25
2022 | 50         | 28         | 22
...
```

## Notes

- Total always equals 100%
- Shows relative proportions, not absolute values
- Good for composition changes over time
- Each area width shows percentage contribution
