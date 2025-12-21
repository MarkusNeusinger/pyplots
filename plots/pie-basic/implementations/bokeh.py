""" pyplots.ai
pie-basic: Basic Pie Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
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

# Calculate start and end angles for each slice (counter-clockwise from top)
# Bokeh wedges are drawn counter-clockwise, so start_angle < end_angle
start_angles = []
end_angles = []
current_angle = math.pi / 2  # Start from top (90 degrees)
for angle in angles:
    end_angle = current_angle
    start_angle = current_angle - angle  # End before start for CCW order
    start_angles.append(start_angle)
    end_angles.append(end_angle)
    current_angle = start_angle  # Continue from where we left off

# Colors - Python Blue and Yellow first, then distinct colorblind-safe palette
colors = ["#306998", "#FFD43B", "#E74C3C", "#9B59B6", "#27AE60"]

# Calculate label positions (middle of each slice)
mid_angles = [(start_angles[i] + end_angles[i]) / 2 for i in range(len(categories))]
radius = 0.85  # Pie radius
label_radius = radius * 0.65  # Labels at 65% of radius

# Explosion offset for the largest slice (Engineering at index 0)
explode_radius = 0.05
explode_index = 0  # Engineering is the largest

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
    # Apply explosion offset to the largest slice
    if i == explode_index:
        offset_x = explode_radius * math.cos(mid_angles[i])
        offset_y = explode_radius * math.sin(mid_angles[i])
    else:
        offset_x = 0
        offset_y = 0

    r = p.wedge(
        x=offset_x,
        y=offset_y,
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
    # Account for explosion offset in label position
    if i == explode_index:
        offset_x = explode_radius * math.cos(mid_angles[i])
        offset_y = explode_radius * math.sin(mid_angles[i])
    else:
        offset_x = 0
        offset_y = 0

    x = label_radius * math.cos(mid_angles[i]) + offset_x
    y = label_radius * math.sin(mid_angles[i]) + offset_y
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
    label_text_font_size="28pt",
    glyph_width=50,
    glyph_height=50,
    spacing=25,
    padding=40,
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
