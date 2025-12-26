# polar-scatter: Polar Scatter Plot

## Description

A scatter plot displayed in polar coordinates where data points are positioned using angle (theta) and radius (r) rather than Cartesian x and y coordinates. This visualization is particularly effective for cyclical or directional data where the angular component carries meaningful information.

## Applications

- **Wind analysis**: Visualizing wind direction and speed measurements
- **Cyclical patterns**: Showing time-of-day or seasonal patterns
- **Directional data**: Analyzing compass bearings or orientations
- **Periodic phenomena**: Displaying data with natural angular relationships
- **Geographic orientation**: Mapping directional measurements relative to a center point

## Data

Generate synthetic wind measurement data with the following characteristics:
- 100-150 data points representing wind observations
- Angle (theta): Wind direction in degrees (0-360)
- Radius: Wind speed in appropriate units (e.g., m/s or knots)
- Optional: Color encoding for a third variable (e.g., temperature or time of day)
- Use realistic distributions (wind often has prevailing directions)

Example structure:
```
angle (degrees) | radius (speed) | category (optional)
45              | 12.5           | morning
180             | 8.3            | afternoon
270             | 15.2           | morning
```

## Notes

- Use radians internally for calculations, but display degrees for readability
- Include clear radial gridlines at regular intervals
- Add angular tick marks at meaningful intervals (0°, 90°, 180°, 270° or similar)
- Consider using different markers or colors for data categories
- Ensure the plot is properly centered with appropriate padding
- The radius axis should start at 0 and extend to accommodate all data points
- Add appropriate title and legend if using color encoding
