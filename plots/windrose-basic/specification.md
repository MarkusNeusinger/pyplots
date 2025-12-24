# windrose-basic: Wind Rose Chart

## Description

A wind rose displays wind speed and direction data as a polar stacked histogram showing the frequency distribution of wind across compass directions. Each spoke represents a direction sector (typically 8-16 bins), with stacked colored segments indicating different wind speed ranges. This specialized meteorological visualization reveals dominant wind patterns, prevailing directions, and speed distributions simultaneously, making it essential for site assessment and environmental analysis.

## Applications

- Assessing wind farm site suitability by analyzing prevailing wind patterns and speed distributions
- Planning airport runway orientations based on historical wind direction frequencies
- Conducting air quality studies to understand pollutant dispersion patterns
- Designing building ventilation and urban planning based on local wind climatology

## Data

- `direction` (numeric) - Wind direction in degrees (0-360, where 0/360 is North)
- `speed` (numeric) - Wind speed in consistent units (m/s, km/h, or knots)
- `frequency` (numeric, optional) - Pre-aggregated frequency counts per direction/speed bin
- Size: 500-50000 observations recommended for meaningful distributions
- Example: Hourly wind measurements from a weather station over one year

## Notes

- Direction bins typically use 8 (N, NE, E, SE, S, SW, W, NW) or 16 sectors
- Speed bins should use meaningful ranges for the data (e.g., 0-5, 5-10, 10-15, 15+ m/s)
- North should be at the top (0 degrees) following meteorological convention
- Colors traditionally progress from cool (calm) to warm (strong) for speed bins
- Include a legend showing speed ranges and their colors
- Radial axis shows frequency (percentage or count) of observations per direction
