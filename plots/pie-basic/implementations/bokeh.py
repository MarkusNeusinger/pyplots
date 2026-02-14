"""pyplots.ai
pie-basic: Basic Pie Chart
Library: bokeh 3.8.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

import math

from bokeh.io import export_png, output_file, save
from bokeh.models import Label, Legend, LegendItem
from bokeh.plotting import figure


# Data - Cloud infrastructure market share (2024)
categories = ["AWS", "Azure", "Google Cloud", "Alibaba", "Others"]
values = [31, 25, 11, 4, 29]

# Compute angles and percentages
total = sum(values)
percentages = [v / total * 100 for v in values]
angles = [v / total * 2 * math.pi for v in values]

# Start/end angles (clockwise from top)
start_angles = []
end_angles = []
current = math.pi / 2
for a in angles:
    start_angles.append(current)
    current -= a
    end_angles.append(current)

mid_angles = [(s + e) / 2 for s, e in zip(start_angles, end_angles, strict=True)]

# Explode the largest slice (AWS) for emphasis
explode_idx = 0
explode_r = 0.05
offsets_x = [0.0] * len(categories)
offsets_y = [0.0] * len(categories)
offsets_x[explode_idx] = explode_r * math.cos(mid_angles[explode_idx])
offsets_y[explode_idx] = explode_r * math.sin(mid_angles[explode_idx])

# Colors - Python Blue first, colorblind-safe palette
colors = ["#306998", "#FFD43B", "#E74C3C", "#27AE60", "#9B59B6"]

# Create figure (3600 x 3600 px square)
radius = 0.88
p = figure(
    width=3600,
    height=3600,
    title="pie-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_range=(-1.25, 1.25),
    y_range=(-1.15, 1.15),
    tools="",
    toolbar_location=None,
)

# Draw wedges (clockwise from top)
renderers = []
for i in range(len(categories)):
    r = p.wedge(
        x=offsets_x[i],
        y=offsets_y[i],
        radius=radius,
        start_angle=start_angles[i],
        end_angle=end_angles[i],
        direction="clock",
        fill_color=colors[i],
        line_color="white",
        line_width=5,
    )
    renderers.append(r)

# Percentage labels on each slice
label_r = radius * 0.6
for i in range(len(categories)):
    lx = label_r * math.cos(mid_angles[i]) + offsets_x[i]
    ly = label_r * math.sin(mid_angles[i]) + offsets_y[i]
    text_color = "#333333" if colors[i] == "#FFD43B" else "white"
    p.add_layout(
        Label(
            x=lx,
            y=ly,
            text=f"{percentages[i]:.0f}%",
            text_font_size="36pt",
            text_color=text_color,
            text_font_style="bold",
            text_align="center",
            text_baseline="middle",
        )
    )

# Legend with category names and percentages
legend_items = [
    LegendItem(label=f"{categories[i]} ({percentages[i]:.0f}%)", renderers=[renderers[i]])
    for i in range(len(categories))
]
legend = Legend(
    items=legend_items,
    location="center",
    orientation="horizontal",
    label_text_font_size="30pt",
    glyph_width=50,
    glyph_height=50,
    spacing=50,
    padding=30,
    background_fill_alpha=0.0,
    border_line_color=None,
)
p.add_layout(legend, "below")

# Styling
p.title.text_font_size = "40pt"
p.title.align = "center"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
