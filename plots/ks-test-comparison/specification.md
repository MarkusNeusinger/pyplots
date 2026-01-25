# ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison

## Description

A Kolmogorov-Smirnov (K-S) plot compares two empirical cumulative distribution functions (ECDFs) and visualizes the K-S statistic, which is the maximum vertical distance between the two distributions. The plot displays both ECDFs as step functions, highlights the point of maximum divergence, and typically reports the K-S statistic value and p-value for hypothesis testing. This visualization is essential for determining whether two samples come from the same underlying distribution.

## Applications

- Model validation in credit scoring, comparing score distributions between Good and Bad customers to assess model discrimination
- A/B testing to verify whether control and treatment groups have statistically different outcome distributions
- Quality control analysis comparing actual product measurements against expected or historical distributions
- Validating that model predictions or residuals follow expected distributions in regression diagnostics

## Data

- `sample1` (numeric array) - First distribution sample (e.g., scores for Good customers, control group values)
- `sample2` (numeric array) - Second distribution sample (e.g., scores for Bad customers, treatment group values)
- Size: 100-1000 points per sample recommended for reliable statistical inference

## Notes

- Display both empirical CDFs as step functions with distinct colors/styles
- Show the K-S statistic value prominently (the maximum vertical distance)
- Highlight the point where the maximum distance occurs with a vertical line or annotation
- Include the p-value from the K-S test to indicate statistical significance
- Label each distribution clearly in a legend
- Y-axis should range from 0 to 1 representing cumulative proportion
