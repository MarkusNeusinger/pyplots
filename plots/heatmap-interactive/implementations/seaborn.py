"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-08

NOTE: This implementation is NOT FEASIBLE.

Seaborn is a static visualization library built on matplotlib.
It cannot implement interactive features required by this specification:
- Hover tooltips showing row/column labels and values
- Zoom/pan capabilities with smooth interaction
- Reset button or double-click to reset view
- Crosshair or highlight effect on hover

For interactive heatmaps, use:
- plotly (px.imshow or go.Heatmap)
- bokeh (figure.rect with HoverTool)
- altair (mark_rect with tooltips)
- highcharts (Highcharts.chart with heatmap series)
"""

# AR-06: NOT_FEASIBLE
# Seaborn cannot implement interactive features natively.
# This specification requires interactivity that is beyond seaborn's capabilities.
raise NotImplementedError(
    "Seaborn cannot implement interactive heatmaps. "
    "This library produces static images only and does not support "
    "hover tooltips, zoom/pan, or other interactive features. "
    "Use plotly, bokeh, altair, or highcharts instead."
)
