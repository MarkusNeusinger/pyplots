# polar-line: Polar Line Plot

## Description

A line plot rendered in polar coordinates, where data points are connected with lines around a circular axis. The angle (theta) typically represents a cyclical variable while the radius shows magnitude.

## Applications

- Cyclical data visualization (hours, months, seasons)
- Directional data with continuous measurements
- Periodic pattern analysis
- Angular velocity or rotation data

## Data

The visualization requires:
- **Theta variable**: Angular position (degrees or radians)
- **Radius variable**: Magnitude/distance from center

Example structure:
```
Angle | Value
------|-------
0     | 4.2
30    | 5.1
60    | 6.3
90    | 5.8
...
```

## Notes

- Line connects points in theta order
- Can show multiple series with different colors
- Often used for time-of-day or seasonal patterns
- Grid lines are concentric circles and radial lines
