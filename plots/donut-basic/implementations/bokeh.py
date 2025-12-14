"""
donut-basic: Basic Donut Chart
Library: bokeh
"""

from math import pi

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure
from bokeh.transform import cumsum


# Data
categories = ["Technology", "Healthcare", "Finance", "Energy", "Retail"]
values = [35, 25, 20, 12, 8]

# Calculate angles for donut segments
data = {
    "category": categories,
    "value": values,
    "angle": [v / sum(values) * 2 * pi for v in values],
    "percentage": [f"{v / sum(values) * 100:.1f}%" for v in values],
}

# Cumulative angles for start/end positions
cumulative = np.cumsum([0] + data["angle"][:-1]).tolist()
data["start_angle"] = cumulative
data["end_angle"] = np.cumsum(data["angle"]).tolist()

# Colors - Python Blue as primary, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3"]
data["color"] = colors

source = ColumnDataSource(data=data)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="donut-basic · bokeh · pyplots.ai",
    toolbar_location=None,
    tools="",
    x_range=(-1.2, 1.8),
    y_range=(-1.2, 1.2),
)

# Draw donut using annular wedge
p.annular_wedge(
    x=0,
    y=0,
    inner_radius=0.4,
    outer_radius=0.9,
    start_angle=cumsum("angle", include_zero=True),
    end_angle=cumsum("angle"),
    line_color="white",
    line_width=3,
    fill_color="color",
    source=source,
)

# Add percentage labels on segments
for pct, start, end in zip(data["percentage"], data["start_angle"], data["end_angle"], strict=True):
    mid_angle = (start + end) / 2
    # Position labels at middle of the ring
    label_radius = 0.65
    x = label_radius * np.cos(mid_angle - pi / 2 + pi)
    y = label_radius * np.sin(mid_angle - pi / 2 + pi)

    label = Label(
        x=x,
        y=y,
        text=pct,
        text_font_size="24pt",
        text_color="white",
        text_font_style="bold",
        text_align="center",
        text_baseline="middle",
    )
    p.add_layout(label)

# Add center text showing total
total = sum(values)
center_label = Label(
    x=0, y=0.05, text="Total", text_font_size="28pt", text_color="#333333", text_align="center", text_baseline="middle"
)
p.add_layout(center_label)

center_value = Label(
    x=0,
    y=-0.1,
    text=str(total),
    text_font_size="40pt",
    text_color="#306998",
    text_font_style="bold",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(center_value)

# Add legend entries on the right
legend_x = 1.15
legend_y_start = 0.5
legend_spacing = 0.2

for i, (cat, val, color) in enumerate(zip(categories, values, colors, strict=True)):
    y_pos = legend_y_start - i * legend_spacing
    # Color box
    p.rect(x=legend_x, y=y_pos, width=0.08, height=0.08, fill_color=color, line_color=None)
    # Label text
    legend_label = Label(
        x=legend_x + 0.08,
        y=y_pos,
        text=f"{cat} ({val})",
        text_font_size="20pt",
        text_color="#333333",
        text_align="left",
        text_baseline="middle",
    )
    p.add_layout(legend_label)

# Style
p.title.text_font_size = "32pt"
p.title.text_color = "#333333"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = None
p.border_fill_color = None

# Save
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
