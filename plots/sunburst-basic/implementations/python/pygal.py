"""anyplot.ai
sunburst-basic: Basic Sunburst Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2026-05-04
"""

import os

import pygal
from pygal.style import Style


THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"

OKABE_ITO = ("#009E73", "#D55E00", "#0072B2", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442")

custom_style = Style(
    background=PAGE_BG,
    plot_background=PAGE_BG,
    foreground=INK,
    foreground_strong=INK,
    foreground_subtle=INK_MUTED,
    colors=OKABE_ITO,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=2,
)

# Organizational budget breakdown (in $K)
# Level 1: Departments (series), Level 2: Teams (items within each series)
chart = pygal.Treemap(
    style=custom_style,
    width=3600,
    height=3600,
    title="sunburst-basic · pygal · anyplot.ai",
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    show_legend=True,
)

chart.add(
    "Technology",
    [
        {"value": 180, "label": "Backend Engineering"},
        {"value": 140, "label": "Frontend Engineering"},
        {"value": 100, "label": "Data Science"},
    ],
)
chart.add(
    "Business", [{"value": 150, "label": "Sales"}, {"value": 100, "label": "Finance"}, {"value": 60, "label": "Legal"}]
)
chart.add("Operations", [{"value": 90, "label": "IT Support"}, {"value": 80, "label": "Human Resources"}])
chart.add("Marketing", [{"value": 60, "label": "Brand Design"}, {"value": 40, "label": "Digital Marketing"}])

# Save
chart.render_to_png(f"plot-{THEME}.png")
with open(f"plot-{THEME}.html", "wb") as f:
    f.write(chart.render())
