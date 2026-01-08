""" pyplots.ai
scatter-brush-zoom: Interactive Scatter Plot with Brush Selection and Zoom
Library: seaborn | Python 3.13
Quality: NOT_FEASIBLE | Created: 2026-01-08

NOT_FEASIBLE: Seaborn is a static visualization library built on matplotlib.
It cannot implement interactive features like:
- Brush selection (click and drag to select rectangular region)
- Zoom functionality via mouse wheel or double-click
- Real-time visual highlighting of selected points
- Pan functionality
- Interactive reset/clear selection buttons

These features require a truly interactive library such as:
- plotly (with lasso/box select and zoom/pan)
- bokeh (with BoxSelectTool, WheelZoomTool, PanTool)
- altair (with interval selection and bind_scales)

Seaborn outputs static PNG images and has no mechanism for handling user
interactions at runtime.
"""
