# histogram-density: Density Histogram

## Description

A density histogram displays the distribution of a continuous variable normalized so that the total area under the histogram equals 1, representing probability density instead of raw counts. This normalization allows direct comparison between distributions with different sample sizes and enables overlaying theoretical probability density functions (PDFs) for statistical analysis.

## Applications

- Comparing empirical distributions across datasets with different sample sizes
- Overlaying theoretical distributions (normal, exponential, etc.) to assess goodness of fit
- Visualizing probability density for statistical inference and hypothesis testing
- Standardizing distribution displays for publication-quality statistical graphics

## Data

- `values` (numeric) - The continuous variable to visualize
- Size: 50-1000 observations recommended for meaningful density estimation
- Example: Test scores, measurement data, financial returns, or any continuous distribution

## Notes

- Y-axis shows density (probability per unit), not count
- Total area under histogram bars equals 1
- Bin width affects visual interpretation; use consistent binning for comparisons
- Consider adding a reference line or theoretical PDF overlay for context
