""" pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure


# Data - Wind direction frequencies (8 compass directions)
np.random.seed(42)
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
angles_deg = np.array([90, 45, 0, 315, 270, 225, 180, 135])  # Math convention (E=0, CCW)
frequencies = np.array([18, 12, 8, 5, 10, 22, 15, 10])  # Wind frequency percentages

# Convert to radians and calculate wedge parameters
angles_rad = np.deg2rad(angles_deg)
bar_width = np.deg2rad(40)  # 40 degrees width for each bar

# Normalize frequencies for radius (max radius = 0.9 to leave room for labels)
max_freq = frequencies.max()
radii = frequencies / max_freq * 0.85

# Colors - using Python Blue with varying alpha for visual interest
colors = ["#306998"] * len(directions)

# Create source for wedges (polar bars)
source = ColumnDataSource(
    data={
        "start_angle": angles_rad - bar_width / 2,
        "end_angle": angles_rad + bar_width / 2,
        "radius": radii,
        "direction": directions,
        "frequency": frequencies,
        "color": colors,
    }
)

# Label positions (outside the bars)
label_radius = 0.95
label_x = label_radius * np.cos(angles_rad)
label_y = label_radius * np.sin(angles_rad)

label_source = ColumnDataSource(data={"x": label_x, "y": label_y, "text": directions})

# Frequency label positions (at bar ends)
freq_label_x = (radii + 0.05) * np.cos(angles_rad)
freq_label_y = (radii + 0.05) * np.sin(angles_rad)
freq_texts = [f"{f}%" for f in frequencies]

freq_label_source = ColumnDataSource(data={"x": freq_label_x, "y": freq_label_y, "text": freq_texts})

# Create figure with square aspect for polar plot
p = figure(
    width=3600,
    height=3600,
    title="polar-bar · bokeh · pyplots.ai",
    x_range=(-1.3, 1.3),
    y_range=(-1.3, 1.3),
    tools="",
    toolbar_location=None,
)

# Draw polar bars as wedges from center
p.wedge(
    x=0,
    y=0,
    radius="radius",
    start_angle="start_angle",
    end_angle="end_angle",
    fill_color="color",
    fill_alpha=0.8,
    line_color="white",
    line_width=3,
    source=source,
)

# Add concentric circles for reference (like polar grid)
for r in [0.25, 0.5, 0.75]:
    theta = np.linspace(0, 2 * np.pi, 100)
    circle_x = r * np.cos(theta)
    circle_y = r * np.sin(theta)
    p.line(circle_x, circle_y, line_color="gray", line_alpha=0.3, line_width=2)

# Add radial lines from center to edge
for angle in angles_rad:
    p.line([0, 0.9 * np.cos(angle)], [0, 0.9 * np.sin(angle)], line_color="gray", line_alpha=0.3, line_width=2)

# Add direction labels around the outside
direction_labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_font_size="28pt",
    text_color="#306998",
    text_font_style="bold",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(direction_labels)

# Add frequency labels at bar ends
freq_labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=freq_label_source,
    text_font_size="20pt",
    text_color="#333333",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(freq_labels)

# Style the plot
p.title.text_font_size = "36pt"
p.title.align = "center"
p.title.text_color = "#306998"

# Hide axes for polar appearance
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None

# Background
p.background_fill_color = "white"

# Save outputs
export_png(p, filename="plot.png")

# Also save HTML for interactive version
output_file("plot.html", title="polar-bar · bokeh · pyplots.ai")
save(p)
