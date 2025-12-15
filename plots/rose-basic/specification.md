# rose-basic: Basic Rose Chart

## Description

A rose chart (also called Nightingale or coxcomb diagram) displays categorical data in a circular format where segments are arranged around the center like pie slices, but with radius proportional to the value rather than angle. This visualization excels at showing cyclical or directional patterns where the circular arrangement has natural meaning. The equal-angle wedges make comparison of values across categories intuitive while emphasizing the periodic nature of the data.

## Applications

- Visualizing monthly sales, weather patterns, or other data with natural 12-month cycles
- Displaying wind direction frequency (wind rose) showing how often wind blows from each compass direction
- Comparing day-of-week patterns like customer visits, social media engagement, or energy consumption
- Showing hourly distributions where the circular clock face arrangement aids interpretation

## Data

- `category` (categorical) - Angular positions representing periodic categories (e.g., months, directions, hours)
- `value` (numeric) - Determines segment radius; larger values extend further from center
- Size: 4-24 categories typical; 8-12 optimal for readability
- Example: Monthly rainfall amounts, wind direction frequencies, or hourly traffic counts

## Notes

- Segment radius should be proportional to value (not area) for easier visual comparison
- Categories should have natural circular ordering (months, compass directions, hours)
- Use consistent color scheme; single color with varying saturation or distinct colors per category
- Start position typically at top (12 o'clock) for time data or north for directional data
- Include radial gridlines to aid value estimation
