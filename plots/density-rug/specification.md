# density-rug: Density Plot with Rug Marks

## Description

A kernel density estimation (KDE) plot combined with rug marks along the x-axis, showing both the smoothed probability distribution and the exact location of each individual data point. This combination provides the best of both worlds: the KDE reveals the overall shape, modality, and smoothed density of the distribution, while the rug marks preserve transparency about where actual observations fall, highlighting data density and potential gaps.

## Applications

- Exploratory data analysis where understanding both distribution shape and raw data placement matters
- Comparing sample distributions while maintaining visibility of actual observation counts and clustering
- Quality control analysis to identify process variations alongside individual measurement locations
- Academic and research presentations requiring both statistical summaries and data transparency

## Data

- `values` (numeric) - The continuous variable to visualize
- Size: 30-500 observations recommended (rug marks become cluttered with very large samples)
- Example: Response times, measurement errors, test scores, or any continuous variable

## Notes

- Display the KDE curve with fill for visual weight and the rug marks as small tick marks along the x-axis
- Use semi-transparent fill under the density curve to avoid obscuring the rug
- Rug marks should be subtle but visible, with slight transparency for overlapping points
- Consider jittering rug marks vertically if using thick ticks to reduce overplotting
