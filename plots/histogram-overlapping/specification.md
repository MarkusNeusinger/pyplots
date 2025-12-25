# histogram-overlapping: Overlapping Histograms

## Description

Overlapping histograms display multiple distributions on the same axes using semi-transparent bars, enabling direct visual comparison between groups. This technique reveals differences in central tendency, spread, and shape across categories while maintaining the familiar histogram format. The transparency allows viewers to see where distributions overlap and diverge.

## Applications

- Comparing test score distributions between control and treatment groups in A/B testing
- Analyzing salary distributions across different departments or job levels
- Visualizing before/after measurement changes in clinical trials or process improvements

## Data

- `values` (numeric) - The continuous variable to visualize
- `group` (categorical) - The grouping variable distinguishing each distribution
- Size: 30-500 observations per group recommended; 2-4 groups work best
- Example: Heights by gender, response times by condition, prices by region

## Notes

- Use semi-transparent fills (alpha ~0.4-0.6) so overlapping regions remain visible
- Assign distinct, contrasting colors to each group
- Include a legend clearly identifying each group
- Align bin edges across all groups for accurate comparison
- Consider using matching bin widths and counts for all distributions
