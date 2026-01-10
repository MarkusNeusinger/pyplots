"""pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-10

NOTE: This specification requires interactive linked brushing/selection across
multiple scatter plots, which pygal cannot implement. pygal's interactivity is
limited to hover tooltips and does not support:
- Linked selection/brushing across charts
- Cross-chart highlighting
- Box or lasso selection
- Dynamic point highlighting based on selections in other views

This implementation provides a static scatter matrix as a best-effort fallback,
but does NOT meet the core interactive requirements of the specification.
"""

# AR-06: NOT_FEASIBLE
# pygal cannot implement interactive linked selection/brushing across subplots.
# The library lacks the following required features:
# 1. No linked selection mechanism between charts
# 2. No brush/lasso selection tools
# 3. No cross-chart highlight synchronization
# 4. No dynamic filtering/selection capabilities
#
# Recommended alternatives: plotly, bokeh, or altair which have native
# linked brushing support for scatter plot matrices.

raise NotImplementedError(
    "pygal cannot implement scatter-matrix-interactive: "
    "The library does not support linked brushing/selection across subplots, "
    "which is the core requirement of this specification. "
    "Use plotly, bokeh, or altair instead for interactive SPLOM with linked selection."
)
