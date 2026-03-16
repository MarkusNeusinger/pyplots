""" pyplots.ai
line-retention-cohort: User Retention Curve by Cohort
Library: pygal 3.1.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Monthly signup cohorts tracked weekly for 12 weeks
np.random.seed(42)

cohorts = {
    "Jan 2025": {"size": 1245, "decay": 0.18},
    "Feb 2025": {"size": 1102, "decay": 0.16},
    "Mar 2025": {"size": 1380, "decay": 0.14},
    "Apr 2025": {"size": 1467, "decay": 0.12},
    "May 2025": {"size": 1590, "decay": 0.11},
}

weeks = list(range(13))
retention_data = {}
for cohort, params in cohorts.items():
    retention = [100.0]
    for week in range(1, 13):
        noise = np.random.normal(0, 1.5)
        prev = retention[-1]
        drop = prev * params["decay"] * (1 / (1 + 0.1 * week)) + noise
        retention.append(max(round(prev - max(drop, 0.5), 1), 5.0))
    retention_data[cohort] = retention

# Style - threshold line first, then cohort colors with higher minimum opacity
colors_with_opacity = (
    "rgba(200, 50, 50, 0.85)",
    "rgba(48, 105, 152, 0.65)",
    "rgba(220, 100, 70, 0.75)",
    "rgba(60, 160, 100, 0.85)",
    "rgba(200, 155, 50, 0.92)",
    "rgba(130, 90, 170, 1.0)",
)

custom_style = Style(
    background="#fafafa",
    plot_background="#fafafa",
    foreground="#2a2a2a",
    foreground_strong="#1a1a1a",
    foreground_subtle="#d8d8d8",
    colors=colors_with_opacity,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=40,
    value_font_size=36,
    opacity=".95",
    opacity_hover="1",
    transition="200ms ease-in",
    font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    title_font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    legend_font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    label_font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    major_label_font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    value_font_family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
)

# Plot
chart = pygal.Line(
    width=4800,
    height=2700,
    title="line-retention-cohort \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Weeks Since Signup",
    y_title="Retained Users (%)",
    style=custom_style,
    show_dots=True,
    dots_size=6,
    stroke_style={"width": 3},
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    truncate_legend=-1,
    range=(0, 105),
    x_label_rotation=0,
    value_formatter=lambda x: f"{x:.0f}%" if x is not None else "",
    tooltip_fancy_mode=True,
    tooltip_border_radius=6,
    interpolate="cubic",
    show_minor_x_labels=False,
    y_labels=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    margin_top=40,
    margin_bottom=60,
    spacing=30,
)

chart.x_labels = [str(w) for w in weeks]
chart.x_labels_major = ["0", "3", "6", "9", "12"]

# Add reference threshold line at 20% retention - bold and visible
chart.add(
    "\u2500\u2500 20% Retention Threshold",
    [20.0] * len(weeks),
    stroke_style={"width": 3, "dasharray": "16, 8"},
    show_dots=False,
    dots_size=0,
)

# Add cohorts with increasing stroke width for newer cohorts
stroke_widths = [3, 3.5, 4, 5, 7]
dot_sizes = [4, 5, 5, 6, 8]
cohort_list = list(cohorts.items())

for i, (cohort, params) in enumerate(cohort_list):
    label = f"{cohort} (n={params['size']:,})"
    chart.add(
        label,
        [
            {"value": v, "label": f"Week {w}: {v:.1f}% retained"}
            for w, v in zip(weeks, retention_data[cohort], strict=True)
        ],
        stroke_style={"width": stroke_widths[i]},
        dots_size=dot_sizes[i],
    )

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
