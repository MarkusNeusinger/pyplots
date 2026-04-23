"""anyplot.ai
scatter-basic: Basic Scatter Plot
Library: pygal 3.1.0 | Python 3.14
Quality: pending | Updated: 2026-04-23
"""

import os
import sys

import numpy as np


# Avoid name collision between this script (pygal.py) and the pygal package
_here = sys.path[0] if sys.path and sys.path[0] else "."
if _here in sys.path:
    sys.path.remove(_here)

import pygal  # noqa: E402
from pygal.style import Style  # noqa: E402


# Theme tokens (see prompts/default-style-guide.md)
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#8A8A82" if THEME == "light" else "#6E6D66"

OKABE_ITO = ("#009E73", "#D55E00", "#0072B2", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442")

# Data — study hours vs exam scores (realistic educational context, ~0.7 correlation)
np.random.seed(42)
n = 140
study_hours = np.random.uniform(1, 12, n)
exam_scores = np.clip(40 + study_hours * 4.8 + np.random.normal(0, 7, n), 30, 100)

# Style
custom_style = Style(
    background=PAGE_BG,
    plot_background=PAGE_BG,
    foreground=INK,
    foreground_strong=INK,
    foreground_subtle=INK_MUTED,
    colors=OKABE_ITO,
    font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_size=28,
    label_font_size=22,
    major_label_font_size=18,
    legend_font_size=16,
    value_font_size=14,
    opacity=0.7,
    opacity_hover=0.95,
    stroke_opacity=0,
    stroke_opacity_hover=0,
)

# Chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-basic · pygal · anyplot.ai",
    x_title="Study Hours per Week",
    y_title="Exam Score (%)",
    stroke=False,
    dots_size=14,
    show_legend=False,
    show_x_guides=True,
    show_y_guides=True,
    xrange=(0, 13),
    range=(25, 105),
    margin=60,
)

chart.add("Students", [(float(h), float(s)) for h, s in zip(study_hours, exam_scores, strict=True)])

# Save
chart.render_to_png(f"plot-{THEME}.png")
with open(f"plot-{THEME}.html", "wb") as f:
    f.write(chart.render())
