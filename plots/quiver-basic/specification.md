# quiver-basic: Basic Quiver Plot

## Description

A quiver plot displays vector fields using arrows positioned at grid points. Each arrow represents a vector at that location, with direction indicating the vector's angle and length proportional to its magnitude. This visualization reveals flow patterns, gradients, and field structure in two-dimensional data.

## Applications

- Visualizing wind patterns or ocean currents in meteorology and oceanography
- Displaying electromagnetic field lines in physics simulations
- Showing gradient descent directions in optimization landscapes
- Illustrating fluid flow patterns in computational fluid dynamics

## Data

- `x` (numeric array) - X-coordinates of arrow positions on a grid
- `y` (numeric array) - Y-coordinates of arrow positions on a grid
- `u` (numeric array) - Horizontal component (dx) of each vector
- `v` (numeric array) - Vertical component (dy) of each vector
- Size: Typically 10x10 to 20x20 grid (100-400 arrows) for visual clarity
- Example: A 2D flow field such as `u = -y, v = x` creates a circular rotation pattern

## Notes

- Arrow spacing should be uniform and sufficient to prevent overlap
- Arrow length should be scaled appropriately so vectors are distinguishable
- Consider using a simple mathematical function (like rotation or gradient) to generate sample data
- Optional: color can encode magnitude for additional insight
