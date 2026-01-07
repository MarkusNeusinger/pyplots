# line-3d-trajectory: 3D Line Plot for Trajectory Visualization

## Description

A 3D line plot that displays paths, trajectories, or curves as connected lines in three-dimensional space. Unlike scatter plots that show discrete points, this visualization connects data points sequentially to reveal continuous paths, making it ideal for understanding motion, mathematical curves, and temporal evolution in 3D. Interactive rotation is essential for exploring the spatial structure of complex trajectories.

## Applications

- Visualizing particle trajectories and orbital mechanics in physics simulations
- Plotting flight paths, drone routes, or vehicle navigation in aerospace and robotics
- Displaying mathematical curves like helices, spirals, and chaotic attractors (Lorenz, Rossler)
- Analyzing time series data embedded in 3D feature spaces for pattern recognition

## Data

- `x` (numeric array) - X-coordinate values along the trajectory path
- `y` (numeric array) - Y-coordinate values along the trajectory path
- `z` (numeric array) - Z-coordinate values along the trajectory path
- `color` (numeric or categorical, optional) - Variable for color encoding (time progression or category)
- Size: 100-2000 points for smooth trajectory visualization
- Example: A parametric helix or Lorenz attractor trajectory

## Notes

- Points should be connected with smooth lines in sequential order
- Color gradients can effectively show time progression or parameter evolution
- Multiple trajectories with different colors help compare paths or initial conditions
- Interactive rotation and zoom are critical for understanding 3D spatial relationships
- Consider line width and transparency for overlapping trajectory segments
