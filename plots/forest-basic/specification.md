# forest-basic: Meta-Analysis Forest Plot

## Description

A forest plot displays effect sizes with confidence intervals from multiple studies in a meta-analysis. Each study is represented as a point estimate with horizontal whiskers showing the confidence interval, and a diamond at the bottom shows the pooled estimate. The plot includes a vertical reference line at the null effect (typically 0 or 1), making it easy to assess statistical significance and heterogeneity across studies.

## Applications

- Summarizing results from systematic reviews in medical research
- Comparing treatment effects across multiple clinical trials
- Visualizing heterogeneity and consistency of findings across studies
- Presenting pooled effect estimates with confidence intervals

## Data

- `study` (str) - Study name or identifier
- `effect_size` (float) - Point estimate of the effect (e.g., odds ratio, risk ratio, mean difference)
- `ci_lower` (float) - Lower bound of the confidence interval
- `ci_upper` (float) - Upper bound of the confidence interval
- `weight` (float, optional) - Study weight for visual sizing of markers
- Size: 5-30 studies
- Example: Meta-analysis of randomized controlled trials comparing treatment vs control

## Notes

- Diamond shape for the pooled/overall estimate at the bottom
- Vertical reference line at null effect (0 for mean difference, 1 for ratios)
- Marker size proportional to study weight when provided
- Studies typically ordered by effect size or chronologically
- Clear axis labels showing the effect measure and scale
