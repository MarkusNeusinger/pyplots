# ternary-density: Ternary Density Plot

## Description

A ternary density plot combines a three-component ternary diagram with kernel density estimation to visualize where compositional data concentrates. Instead of showing individual points, this visualization uses a heatmap overlay to reveal the underlying probability distribution of compositions, making it ideal for identifying clusters, modes, and patterns in large compositional datasets.

## Applications

- Analyzing sediment composition distributions across geological samples (sand/silt/clay)
- Visualizing alloy mixture preferences in materials science research
- Identifying common flavor profiles in food science (sweet/sour/bitter ratios)
- Understanding market positioning patterns among three competing attributes

## Data

- `component_a` (numeric) - Proportion of first component (0-100%)
- `component_b` (numeric) - Proportion of second component (0-100%)
- `component_c` (numeric) - Proportion of third component (0-100%)
- Size: 100-5000 points ideal for density estimation; fewer points may yield sparse density
- Constraint: All three components must sum to 100% (or a constant total)

## Notes

- Use a perceptually uniform colormap (viridis, plasma) for the density overlay
- Grid lines should be visible beneath the density layer with appropriate transparency
- Each vertex should be clearly labeled with component names
- Consider showing contour lines at key density levels for easier interpretation
- Bandwidth selection for KDE affects smoothness; auto-selection methods work well for most cases
