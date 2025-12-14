# radar-basic: Basic Radar Chart

## Description

A radar chart (also known as spider or web chart) displays multivariate data on axes starting from a common center point, with values connected to form a polygon. Each axis represents a different variable, making it ideal for comparing multiple quantitative variables at once or visualizing strengths and weaknesses across categories.

## Applications

- Employee performance reviews showing scores across multiple competencies (communication, technical skills, teamwork, etc.)
- Product feature comparisons across attributes like price, quality, durability, and ease of use
- Sports player statistics comparing metrics such as speed, strength, accuracy, and stamina
- Company benchmarking across key performance indicators

## Data

- `category` (string) - axis labels representing different variables/dimensions
- `value` (numeric) - values for each axis (0-100 scale recommended for clarity)
- Size: 4-8 axes, 1-3 series for comparison

## Notes

- Use filled polygons with transparency (alpha ~0.25) for overlap visibility when comparing multiple series
- Include gridlines at regular intervals (e.g., 20, 40, 60, 80, 100)
- Label each axis clearly at the outer edge
- Use distinct colors for multiple series with a legend
- Close the polygon by connecting the last point back to the first
