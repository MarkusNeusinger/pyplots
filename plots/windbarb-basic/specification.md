# windbarb-basic: Wind Barb Plot for Meteorological Data

## Description

A wind barb plot displays wind speed and direction at specific locations using standard meteorological barb notation. Each barb consists of a staff pointing in the direction from which the wind blows, with short barbs (5 knots), long barbs (10 knots), and triangular pennants (50 knots) attached to indicate speed. This internationally recognized symbology enables rapid interpretation of wind patterns across weather maps and atmospheric data visualizations.

## Applications

- Displaying surface wind observations across weather station networks on synoptic maps
- Visualizing upper-air wind patterns from radiosonde or pilot balloon observations
- Showing wind field data from numerical weather prediction model output
- Presenting aviation weather information for flight planning and meteorological briefings

## Data

- `x` (numeric) - X-coordinate or longitude for barb position
- `y` (numeric) - Y-coordinate or latitude for barb position
- `u` (numeric) - Zonal (east-west) wind component in knots or m/s
- `v` (numeric) - Meridional (north-south) wind component in knots or m/s
- Size: 20-200 barbs recommended for clear visualization without overlap
- Example: Surface wind observations from a grid of weather stations

## Notes

- Wind barbs point in the direction FROM which the wind blows (opposite to arrow convention)
- Standard notation: half barb = 5 knots, full barb = 10 knots, pennant (triangle) = 50 knots
- Barbs are added on the left side of the staff in the Northern Hemisphere
- Calm winds (< 2.5 knots) shown as an open circle without a staff
- Grid spacing should prevent barb overlap for readability
- Consider using a map projection background for geographic data
