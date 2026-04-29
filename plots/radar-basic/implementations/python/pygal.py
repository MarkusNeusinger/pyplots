""" anyplot.ai
radar-basic: Basic Radar Chart
Library: pygal 3.1.0 | Python 3.13.13
Quality: 79/100 | Updated: 2026-04-29
"""

import importlib
import os
import sys


# Prevent this file (pygal.py) from shadowing the installed pygal package
_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p) != _here]

pygal = importlib.import_module("pygal")
Style = importlib.import_module("pygal.style").Style

THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"

OKABE_ITO = ("#009E73", "#D55E00", "#0072B2", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442")

# Data - Employee performance comparison across competencies
categories = ["Communication", "Technical Skills", "Teamwork", "Problem Solving", "Leadership", "Creativity"]

employee_a = [85, 92, 78, 88, 72, 80]
employee_b = [75, 68, 90, 82, 85, 78]

# Style
custom_style = Style(
    background=PAGE_BG,
    plot_background=PAGE_BG,
    foreground=INK,
    foreground_strong=INK,
    foreground_subtle=INK_MUTED,
    colors=OKABE_ITO,
    title_font_size=28,
    label_font_size=18,
    major_label_font_size=16,
    legend_font_size=16,
    value_font_size=14,
    opacity=0.25,
    opacity_hover=0.5,
)

# Plot
chart = pygal.Radar(
    width=3600,
    height=3600,
    style=custom_style,
    title="radar-basic · pygal · anyplot.ai",
    show_legend=True,
    legend_at_bottom=True,
    fill=True,
    dots_size=6,
    stroke_style={"width": 4},
    show_y_guides=True,
    y_labels_major_every=2,
)

chart.x_labels = categories
chart.add("Employee A", employee_a)
chart.add("Employee B", employee_b)

# Save
chart.render_to_png(f"plot-{THEME}.png")
with open(f"plot-{THEME}.html", "wb") as f:
    f.write(chart.render())
