# polar-bar: Polar Bar Chart (Wind Rose)

## Description

A bar chart arranged in a circle with bars radiating outward from the center. Each bar's angle represents a category (often direction) and length represents magnitude. Commonly used as a wind rose for meteorological data.

## Applications

- Wind direction and speed distribution
- Directional frequency analysis
- Cyclical category comparisons
- Compass-based data visualization

## Data

The visualization requires:
- **Direction variable**: Angular categories (N, NE, E, SE, S, SW, W, NW or degrees)
- **Magnitude variable**: Bar height/frequency

Example structure:
```
Direction | Frequency
----------|----------
N         | 15
NE        | 8
E         | 12
SE        | 5
...
```

## Notes

- Bars extend outward from center
- Can be stacked for multiple categories (e.g., wind speed ranges)
- Often uses 8 or 16 compass directions
- Color can encode additional variables
