# scatter-complex-plane: Complex Plane Visualization (Argand Diagram)

## Description

An Argand diagram plots complex numbers as points in the complex plane, with the real part on the x-axis and the imaginary part on the y-axis. Vectors from the origin to each point illustrate magnitude and phase angle, while a unit circle provides a geometric reference. This visualization is foundational for complex analysis, signal processing, and understanding operations like addition, multiplication, and roots of unity geometrically.

## Applications

- Visualizing roots of polynomials in the complex plane to understand factorization and zero distribution
- Showing nth roots of unity arranged symmetrically on the unit circle for number theory and FFT education
- Illustrating complex transformations such as rotation and scaling by multiplying with a complex factor
- Teaching Euler's formula and the relationship between rectangular (a+bi) and polar (r, theta) representations

## Data

- `real` (numeric) - Real part of each complex number (x-coordinate)
- `imaginary` (numeric) - Imaginary part of each complex number (y-coordinate)
- `label` (string, optional) - Point labels such as z1, z2, z1+z2, or symbolic names
- Size: 5-50 complex numbers
- Example: A set of complex numbers including 3rd roots of unity, their sum, and a few arbitrary points with vector arrows and annotations

## Notes

- Draw real (horizontal) and imaginary (vertical) axes through the origin with labeled tick marks
- Show the unit circle as a dashed reference circle centered at the origin
- Draw vectors (arrows) from the origin to each complex number point
- Equal aspect ratio is required so the unit circle appears circular
- Annotate each point with its rectangular form (a+bi) and optionally polar form (r angle theta)
- Use distinct colors or markers to differentiate categories of points (e.g., roots of unity vs. arbitrary points)
