# bar-categorical: Categorical Count Bar Chart

## Description

A bar chart that automatically counts the frequency of each category in a dataset. Unlike basic bar charts that plot pre-computed values, this chart takes raw categorical data and computes the counts.

## Applications

- Frequency distribution of categorical variables
- Survey response tallying
- Event occurrence counts by type
- Category popularity analysis

## Data

The visualization requires:
- **Categorical variable**: Raw category values (counts computed automatically)

Example structure:
```
Category
--------
A
B
A
C
A
B
...
```

## Notes

- Y-axis shows count/frequency
- Categories displayed on x-axis
- Can optionally sort by count (descending)
- Similar to histogram but for categorical data
