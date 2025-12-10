# radar-basic: Basic Radar Chart

## Description

A radar chart (also known as spider chart or web chart) displays multivariate data on a two-dimensional chart with multiple axes starting from the same central point. Each axis represents a different variable, and data points are connected to form a polygon, making it easy to compare entities across multiple dimensions at a glance.

## Applications

- Comparing product features across competitors in market analysis
- Visualizing athlete performance metrics across different skills (speed, strength, endurance)
- Displaying skill assessment profiles for employees or candidates
- Analyzing strengths and weaknesses in business SWOT-style evaluations

## Data

- `variable` (string) - Name of each dimension/axis (3-8 variables recommended)
- `value` (numeric) - Score for each variable, normalized to 0-100 scale
- `entity` (string) - Optional label for the data series when comparing multiple entities
- Size: 3-8 dimensions per entity, 1-4 entities for comparison
- Example: Performance metrics like ["Speed", "Power", "Accuracy", "Stamina", "Technique"] with corresponding scores

## Notes

- Axes should radiate evenly from the center point
- Values should be normalized to a common scale (typically 0-100) for meaningful comparison
- Consider using semi-transparent fills when overlaying multiple polygons
- Include a legend when displaying multiple entities
- Grid lines or concentric circles help readers estimate values
