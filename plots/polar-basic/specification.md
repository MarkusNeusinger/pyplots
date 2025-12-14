# polar-basic: Basic Polar Chart

## Description

A polar chart displays data points on a circular coordinate system where position is determined by angle (theta) and distance from center (radius). This visualization is ideal for cyclical patterns, directional data, or any dataset where angular relationships are meaningful. It reveals periodic trends and directional distributions that would be obscured in Cartesian coordinates.

## Applications

- Displaying wind speed and direction measurements from weather stations
- Visualizing time-of-day patterns (e.g., website traffic by hour, energy consumption cycles)
- Showing compass-based data such as animal migration directions or survey response distributions
- Analyzing seasonal patterns where the circular nature emphasizes yearly cycles

## Data

- `theta` (numeric) - Angular position in degrees (0-360) or radians (0-2π)
- `radius` (numeric) - Distance from center, representing the measured value
- `category` (string, optional) - Labels or groups for data points
- Size: 12-100 points recommended for clarity
- Example: Hourly temperature readings, wind direction frequency, or activity levels by hour

## Notes

- Radial gridlines should be clearly visible but not overwhelming
- Angular labels should be at standard intervals (0°, 90°, 180°, 270° or compass directions)
- Consider starting angle at top (90°) for time-based data or at right (0°) for standard mathematical convention
- Use appropriate radial scale that doesn't compress data near the center
