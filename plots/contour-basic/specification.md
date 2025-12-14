# contour-basic: Basic Contour Plot

## Description

A contour plot displays isolines (level curves) of a 2D scalar field, connecting points of equal value across a surface. It transforms 3D data into an intuitive 2D representation, making it easy to identify regions of high and low values, gradients, and patterns. Contour plots are essential for visualizing continuous surfaces where the relationship between X, Y coordinates and a Z value needs to be understood.

## Applications

- Visualizing topographic elevation maps to show terrain features like hills, valleys, and ridges
- Displaying temperature or pressure distributions across a geographic region in meteorology
- Analyzing probability density functions or statistical distributions in 2D space
- Mapping chemical concentration gradients in scientific experiments

## Data

- `x` (numeric) - X-axis coordinates forming a regular grid
- `y` (numeric) - Y-axis coordinates forming a regular grid
- `z` (numeric) - Scalar values at each (x, y) grid point representing the surface height
- Size: Grid of 20x20 to 100x100 points
- Example: Mathematical function z = f(x, y) evaluated on a meshgrid, or interpolated measurement data

## Notes

- Use a diverging or sequential colormap appropriate for the data (e.g., viridis, coolwarm)
- Include a colorbar to show the value scale
- Consider using both contour lines and filled regions for clarity
- Label key contour levels when practical
- Ensure sufficient grid resolution for smooth contours
