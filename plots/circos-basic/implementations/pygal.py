"""pyplots.ai
circos-basic: Circos Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

# AR-06 NOT_FEASIBLE: pygal cannot implement Circos plots
# Circos plots require ribbon/arc connections between segments.
# pygal has no chart type that supports chord-style connections.
# Available pygal charts: Bar, Box, Dot, Funnel, Gauge, Histogram, Line, Pie,
# Pyramid, Radar, SolidGauge, Treemap, XY - none support inter-segment ribbons.

raise NotImplementedError(
    "pygal cannot implement Circos plots. "
    "Circos requires ribbon connections between segments (source → target → value), "
    "but pygal has no chart type supporting chord-style or arc connections. "
    "This is AR-06: NOT_FEASIBLE."
)
