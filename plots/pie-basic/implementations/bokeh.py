"""
pie-basic: Basic Pie Chart
Library: bokeh
"""

import math

from bokeh.io import export_png, output_file, save
from bokeh.models import Label, Legend, LegendItem
from bokeh.plotting import figure


# Data - Budget allocation by department
categories = ["Engineering", "Marketing", "Sales", "Operations", "HR"]
values = [35, 25, 20, 12, 8]

# Calculate angles and percentages
total = sum(values)
percentages = [v / total * 100 for v in values]
angles = [v / total * 2 * math.pi for v in values]

# Calculate start and end angles for each slice
start_angles = []
end_angles = []
current_angle = math.pi / 2  # Start from top (90 degrees)
for angle in angles:
    start_angles.append(current_angle)
    current_angle -= angle  # Go clockwise
    end_angles.append(current_angle)

# Colors - Python Blue and Yellow first, then distinct colorblind-safe palette
colors = ["#306998", "#FFD43B", "#E74C3C", "#9B59B6", "#27AE60"]

# Calculate label positions (middle of each slice)
mid_angles = [(start_angles[i] + end_angles[i]) / 2 for i in range(len(categories))]
radius = 0.85  # Pie radius
label_radius = radius * 0.65  # Labels at 65% of radius

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="pie-basic · bokeh · pyplots.ai",
    x_range=(-1.3, 1.8),
    y_range=(-1.15, 1.15),
    tools="",
    toolbar_location=None,
)

# Draw pie wedges and collect renderers for legend
renderers = []
for i in range(len(categories)):
    r = p.wedge(
        x=0,
        y=0,
        radius=radius,
        start_angle=start_angles[i],
        end_angle=end_angles[i],
        fill_color=colors[i],
        line_color="white",
        line_width=4,
    )
    renderers.append(r)

# Add percentage labels on slices
for i in range(len(categories)):
    x = label_radius * math.cos(mid_angles[i])
    y = label_radius * math.sin(mid_angles[i])
    # Use dark text for yellow slice, white for others
    text_color = "#333333" if colors[i] == "#FFD43B" else "white"
    label = Label(
        x=x,
        y=y,
        text=f"{percentages[i]:.1f}%",
        text_font_size="28pt",
        text_color=text_color,
        text_font_style="bold",
        text_align="center",
        text_baseline="middle",
    )
    p.add_layout(label)

# Create legend items
legend_items = [
    LegendItem(label=f"{categories[i]} ({percentages[i]:.1f}%)", renderers=[renderers[i]])
    for i in range(len(categories))
]
legend = Legend(
    items=legend_items,
    location="center_right",
    label_text_font_size="24pt",
    glyph_width=40,
    glyph_height=40,
    spacing=20,
    padding=30,
    background_fill_alpha=0.9,
    border_line_color="#cccccc",
)
p.add_layout(legend, "right")

# Styling
p.title.text_font_size = "36pt"
p.title.align = "center"

# Hide axes and grid for pie chart
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Save outputs
export_png(p, filename="plot.png")

# Also save interactive HTML
output_file("plot.html")
save(p)
