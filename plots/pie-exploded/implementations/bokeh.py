"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure, output_file, save


# Data - Market share example with one dominant player to explode
categories = ["Tech Giant", "Startup A", "Startup B", "Others", "Legacy Corp"]
values = np.array([42, 18, 15, 14, 11])
explode = np.array([0.1, 0, 0, 0, 0])  # Explode the largest slice

# Colors - Python Blue primary, then distinct colorblind-safe colors
colors = ["#306998", "#FFD43B", "#4DAF4A", "#984EA3", "#FF7F00"]

# Calculate angles
total = values.sum()
percentages = values / total * 100
angles = values / total * 2 * np.pi

# Calculate start and end angles for each wedge
start_angles = np.zeros(len(values))
end_angles = np.zeros(len(values))
cumulative = 0
for i in range(len(values)):
    start_angles[i] = cumulative
    cumulative += angles[i]
    end_angles[i] = cumulative

# Calculate mid-angles for explosion offset and label positioning
mid_angles = (start_angles + end_angles) / 2

# Calculate explosion offsets
radius = 0.35  # Base radius of pie
center_x, center_y = 0.5, 0.5  # Center of the chart

# Calculate wedge centers with explosion
x_offsets = explode * np.cos(mid_angles)
y_offsets = explode * np.sin(mid_angles)

# Create figure - Square format for pie chart (3600x3600)
p = figure(
    width=3600,
    height=3600,
    title="pie-exploded · bokeh · pyplots.ai",
    x_range=(-0.1, 1.1),
    y_range=(-0.1, 1.1),
    tools="",
    toolbar_location=None,
)

# Remove grid and axes for clean pie chart appearance
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Title styling
p.title.text_font_size = "36pt"
p.title.align = "center"

# Draw wedges with explosion
for i in range(len(values)):
    cx = center_x + x_offsets[i]
    cy = center_y + y_offsets[i]

    p.wedge(
        x=cx,
        y=cy,
        radius=radius,
        start_angle=start_angles[i],
        end_angle=end_angles[i],
        color=colors[i],
        line_color="white",
        line_width=3,
        legend_label=f"{categories[i]} ({percentages[i]:.1f}%)",
    )

# Add percentage labels on slices
label_radius = radius * 0.65  # Position labels inside the wedges
label_x = []
label_y = []
label_text = []

for i in range(len(values)):
    cx = center_x + x_offsets[i]
    cy = center_y + y_offsets[i]
    lx = cx + label_radius * np.cos(mid_angles[i])
    ly = cy + label_radius * np.sin(mid_angles[i])
    label_x.append(lx)
    label_y.append(ly)
    label_text.append(f"{percentages[i]:.1f}%")

label_source = ColumnDataSource(data={"x": label_x, "y": label_y, "text": label_text})

labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_font_size="24pt",
    text_color="white",
    text_font_style="bold",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(labels)

# Configure legend
p.legend.location = "center_right"
p.legend.label_text_font_size = "28pt"
p.legend.glyph_width = 50
p.legend.glyph_height = 50
p.legend.spacing = 20
p.legend.padding = 30
p.legend.border_line_color = None
p.legend.background_fill_alpha = 0.0

# Save outputs
export_png(p, filename="plot.png")

# Save HTML for interactivity
output_file("plot.html", title="pie-exploded · bokeh · pyplots.ai")
save(p)
