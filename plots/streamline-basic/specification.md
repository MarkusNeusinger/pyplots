# streamline-basic: Basic Streamline Plot

## Description

A streamline plot visualizes vector fields using smooth curves that are tangent to the field at every point. Unlike quiver plots that show discrete arrows, streamlines trace continuous paths through the field, revealing flow patterns, circulation, and field topology. This visualization is ideal for understanding fluid dynamics, electromagnetic fields, or gradient fields where the continuous nature of the flow is important.

## Applications

- Visualizing fluid flow patterns in computational fluid dynamics simulations
- Displaying magnetic or electric field lines in physics and electromagnetic studies
- Showing wind flow patterns in meteorological analysis
- Illustrating gradient descent trajectories in optimization and machine learning

## Data

- `x` (numeric array) - X-coordinates of the grid (1D array for meshgrid)
- `y` (numeric array) - Y-coordinates of the grid (1D array for meshgrid)
- `u` (numeric 2D array) - Horizontal velocity component at each grid point
- `v` (numeric 2D array) - Vertical velocity component at each grid point
- Size: Typically 20x20 to 50x50 grid for smooth streamlines
- Example: A vortex flow field such as `u = -y, v = x` creates circular streamlines

## Notes

- Streamline density should be balanced - too few obscures the pattern, too many creates visual clutter
- Color can encode velocity magnitude or another scalar field along the streamlines
- Line width can optionally vary with field strength for emphasis
- Starting points for streamlines should be distributed to capture the full field structure
