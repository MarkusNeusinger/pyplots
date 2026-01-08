"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08

AR-06: NOT_FEASIBLE

This specification requires interactive selection/brushing with
synchronized highlighting across linked views. pygal is a static SVG
chart library that does not support:
- Interactive selection or brushing
- Cross-chart linking
- Dynamic highlighting based on user selection
- Reset/clear selection functionality

Required features that pygal CANNOT provide:
1. Brush/click selection in any view
2. Synchronized highlighting across views
3. Dynamic point de-emphasis (opacity changes on selection)
4. Reset/clear selection button

For linked views with selection, use: Altair, Bokeh, or Plotly
"""

raise NotImplementedError(
    "pygal cannot implement linked-views-selection. "
    "This specification requires interactive selection/brushing with "
    "synchronized highlighting across linked views. pygal is a static "
    "SVG chart library without interactive selection capabilities. "
    "Use Altair, Bokeh, or Plotly for this visualization type."
)
