"""pyplots.ai
line-3d-trajectory: 3D Line Plot for Trajectory Visualization
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-07

NOT FEASIBLE: plotnine does not support 3D plots.
plotnine is a ggplot2-based grammar of graphics library that only supports 2D visualizations.
3D trajectories, 3D scatter plots, 3D surfaces, and wireframes are not available.
"""

# plotnine cannot implement 3D trajectory plots.
# This specification requires:
# - 3D coordinate system (x, y, z axes)
# - 3D line/path visualization
# - Interactive rotation for exploring 3D spatial relationships
#
# plotnine only supports 2D grammar of graphics and has no 3D capabilities.
# Per the library rules, we should NOT fall back to matplotlib.
#
# AR-06: NOT_FEASIBLE - Library cannot implement this spec natively.

raise NotImplementedError(
    "plotnine does not support 3D plots. "
    "This specification requires 3D trajectory visualization which is not available "
    "in plotnine's grammar of graphics. Use plotly, matplotlib, or bokeh instead."
)
