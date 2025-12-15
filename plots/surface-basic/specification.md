# surface-basic: Basic 3D Surface Plot

## Description

A 3D surface plot visualizes a function of two variables as a continuous surface in three-dimensional space. The height (z-axis) represents the function value at each (x, y) point, with color encoding the same information to enhance depth perception. This visualization is ideal for understanding mathematical functions, terrain data, and response surfaces where the relationship between two inputs and one output needs to be explored.

## Applications

- Visualizing mathematical functions like z = sin(x) * cos(y) or Gaussian surfaces
- Displaying terrain elevation data and topographic maps
- Analyzing response surfaces in optimization and experimental design
- Showing temperature, pressure, or other physical fields across a 2D domain

## Data

- `x` (numeric array) - X-axis grid values, typically uniformly spaced
- `y` (numeric array) - Y-axis grid values, typically uniformly spaced
- `z` (2D numeric array) - Height values at each (x, y) point
- Size: 30x30 to 50x50 grid points for clear visualization

## Notes

- Use a smooth colormap (e.g., viridis, coolwarm) to show height variation
- Include axis labels for x, y, and z dimensions
- Consider adding a colorbar to show the value scale
- For interactive libraries, enable rotation to explore the surface from different angles
