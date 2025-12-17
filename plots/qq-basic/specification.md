# qq-basic: Basic Q-Q Plot

## Description

A Q-Q (Quantile-Quantile) plot compares the distribution of a dataset against a theoretical distribution (typically normal) or another dataset. Points are plotted by matching sample quantiles to theoretical quantiles, with a diagonal reference line indicating perfect distribution match. Deviations from the line reveal distribution characteristics such as skewness, heavy tails, and outliers.

## Applications

- Testing normality assumptions before parametric statistical tests (t-tests, ANOVA, regression)
- Identifying distribution characteristics such as skewness and kurtosis in research datasets
- Quality control analysis to verify process measurements follow expected distributions
- Detecting outliers and data quality issues in experimental data

## Data

- `sample` (numeric) - The observed data values to compare against the reference distribution
- Reference: Normal distribution (default) with parameters estimated from sample
- Size: 30-500 observations recommended for meaningful visual comparison

## Notes

- Points falling along the diagonal reference line indicate data follows the reference distribution
- Systematic deviations reveal specific distribution characteristics: S-curves indicate skewness, curved ends indicate heavy or light tails
- The 45-degree reference line (y=x) should be clearly visible
- Axis labels should indicate "Theoretical Quantiles" and "Sample Quantiles"
