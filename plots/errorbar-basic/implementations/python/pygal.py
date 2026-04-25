"""anyplot.ai
errorbar-basic: Basic Error Bar Plot
Library: pygal | Python 3.13
Quality: 91/100 | Updated: 2026-04-25
"""

import os

import pygal
from pygal.style import Style


# Theme tokens (see prompts/default-style-guide.md)
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"

BRAND = "#009E73"  # Okabe-Ito position 1 — first (and only) series color

# Data - experimental measurements with associated uncertainties
categories = ["Control", "Treatment A", "Treatment B", "Treatment C", "Treatment D", "Treatment E"]
means = [25.3, 38.7, 42.1, 35.8, 48.2, 31.5]
# Asymmetric errors: Treatment C and D have notably different lower/upper bounds
err_lower = [2.1, 3.5, 2.8, 6.5, 4.8, 2.5]
err_upper = [2.1, 3.5, 2.8, 2.8, 2.2, 2.5]

# Style for 4800x2700 canvas
custom_style = Style(
    background=PAGE_BG,
    plot_background=PAGE_BG,
    foreground=INK,
    foreground_strong=INK,
    foreground_subtle=INK_MUTED,
    colors=(BRAND,) * 64,  # repeated so every series shares the brand color
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=40,
    legend_font_size=36,
    value_font_size=28,
    tooltip_font_size=32,
    stroke_width=6,
    opacity=1.0,
    opacity_hover=0.85,
)

# Y-axis zoomed to the data band with breathing room above and below
data_min = min(m - e for m, e in zip(means, err_lower, strict=True))
data_max = max(m + e for m, e in zip(means, err_upper, strict=True))
pad = (data_max - data_min) * 0.15
y_min = max(0.0, data_min - pad)
y_max = data_max + pad

chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    dots_size=24,
    title="errorbar-basic · pygal · anyplot.ai",
    x_title="Experimental Group",
    y_title="Response Value (units)",
    show_legend=False,
    range=(y_min, y_max),
    xrange=(-0.5, len(categories) - 0.5),
    show_x_guides=False,
    show_y_guides=True,
    truncate_label=-1,
    margin=40,
    margin_right=80,
)

chart.x_labels = categories
chart.x_labels_major = categories

cap_width = 0.16  # Width of error bar caps in x-axis units

# Mean points with rich tooltip labels (pygal interactive feature)
mean_points = [
    {"value": (i, means[i]), "label": f"{categories[i]}: {means[i]:.1f} (-{err_lower[i]:.1f}/+{err_upper[i]:.1f})"}
    for i in range(len(means))
]
chart.add("Mean ± error", mean_points, stroke=False, dots_size=28)

# Error bars: separate series per segment for clean line breaks
for i in range(len(means)):
    low = means[i] - err_lower[i]
    high = means[i] + err_upper[i]

    # Vertical error bar
    chart.add(None, [(i, low), (i, high)], stroke=True, show_dots=False)
    # Bottom cap
    chart.add(None, [(i - cap_width, low), (i + cap_width, low)], stroke=True, show_dots=False)
    # Top cap
    chart.add(None, [(i - cap_width, high), (i + cap_width, high)], stroke=True, show_dots=False)

# Save
chart.render_to_png(f"plot-{THEME}.png")
with open(f"plot-{THEME}.html", "wb") as f:
    f.write(chart.render())
