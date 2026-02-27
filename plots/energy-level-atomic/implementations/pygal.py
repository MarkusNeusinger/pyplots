""" pyplots.ai
energy-level-atomic: Atomic Energy Level Diagram
Library: pygal 3.1.0 | Python 3.14.3
Quality: 83/100 | Created: 2026-02-27
"""

import pygal
from pygal.style import Style


# Data - Hydrogen atom energy levels (En = -13.6/n² eV)
energy_values = {n: -13.6 / n**2 for n in range(1, 7)}

# Evenly-spaced visual positions (nonlinear scale for converging upper levels)
visual_y = {1: 1.0, 2: 2.5, 3: 4.0, 4: 5.5, 5: 7.0, 6: 8.5}
ionization_y = 10.0

# Spectral series transitions: (upper_n, lower_n, label)
lyman_transitions = [(2, 1, "Ly-α 122 nm"), (3, 1, "Ly-β 103 nm"), (4, 1, "Ly-γ 97 nm")]
balmer_transitions = [(3, 2, "Hα 656 nm"), (4, 2, "Hβ 486 nm"), (5, 2, "Hγ 434 nm"), (6, 2, "Hδ 410 nm")]

# Layout x-positions
level_x_start = 1.5
level_x_end = 8.5
lyman_x_positions = [2.6, 3.3, 4.0]
balmer_x_positions = [5.8, 6.5, 7.2, 7.9]

# Colors: 6 hidden levels + ionization + 3 Lyman + 4 Balmer
# Energy levels hidden from legend (None title) — 8 visible legend entries
level_color = "#4A5568"
all_colors = (
    (level_color,) * 6 + ("#CC3333",) + ("#7B2FBE", "#9B44D8", "#BB6FE0") + ("#E01030", "#00C8E8", "#3355FF", "#8B11CC")
)

custom_style = Style(
    background="white",
    plot_background="#F8F9FE",
    foreground="#2A2A3A",
    foreground_strong="#1A1A2A",
    foreground_subtle="#E0E0E8",
    colors=all_colors,
    title_font_size=48,
    label_font_size=24,
    major_label_font_size=24,
    legend_font_size=26,
    value_font_size=20,
    stroke_width=4,
)

# Plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Hydrogen Atom \u00b7 energy-level-atomic \u00b7 pygal \u00b7 pyplots.ai",
    y_title="Energy (eV)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    dots_size=16,
    stroke=True,
    margin=80,
    margin_left=240,
    margin_bottom=180,
    margin_top=100,
    range=(0, 11),
    xrange=(0, 10),
    truncate_legend=-1,
    tooltip_border_radius=8,
)

# Y-axis labels showing actual energy values at evenly-spaced positions
chart.y_labels = [
    {"label": "n=1:  \u221213.60 eV", "value": visual_y[1]},
    {"label": "n=2:  \u22123.40 eV", "value": visual_y[2]},
    {"label": "n=3:  \u22121.51 eV", "value": visual_y[3]},
    {"label": "n=4:  \u22120.85 eV", "value": visual_y[4]},
    {"label": "n=5:  \u22120.54 eV", "value": visual_y[5]},
    {"label": "n=6:  \u22120.38 eV", "value": visual_y[6]},
    {"label": "Ionization:  0.00 eV", "value": ionization_y},
]

# Energy level horizontal lines (hidden from legend with None title)
for n in range(1, 7):
    chart.add(
        None,
        [
            {"value": (level_x_start, visual_y[n]), "node": {"r": 0}},
            {"value": (level_x_end, visual_y[n]), "node": {"r": 0}},
        ],
        stroke_style={"width": 3},
    )

# Ionization limit (dashed, prominent)
chart.add(
    "Ionization (0 eV)",
    [
        {"value": (level_x_start - 0.3, ionization_y), "node": {"r": 0}},
        {"value": (level_x_end + 0.3, ionization_y), "node": {"r": 0}},
    ],
    stroke_style={"width": 4, "dasharray": "18, 10"},
)

# Lyman series (UV transitions to n=1) — bold lines with prominent endpoints
lyman_widths = [10, 8, 7]
lyman_nodes = [20, 16, 14]
for i, (upper, lower, label) in enumerate(lyman_transitions):
    x = lyman_x_positions[i]
    chart.add(
        label,
        [
            {"value": (x, visual_y[upper]), "node": {"r": 4}},
            {"value": (x, visual_y[lower]), "node": {"r": lyman_nodes[i]}},
        ],
        stroke_style={"width": lyman_widths[i]},
    )

# Balmer series (visible transitions to n=2) — Hα is the focal point
balmer_widths = [14, 9, 8, 7]
balmer_nodes = [26, 16, 14, 12]
for i, (upper, lower, label) in enumerate(balmer_transitions):
    x = balmer_x_positions[i]
    chart.add(
        label,
        [
            {"value": (x, visual_y[upper]), "node": {"r": 5}},
            {"value": (x, visual_y[lower]), "node": {"r": balmer_nodes[i]}},
        ],
        stroke_style={"width": balmer_widths[i]},
    )

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
