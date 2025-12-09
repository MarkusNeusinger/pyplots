"""
donut-labeled: Donut Chart with Percentage Labels
Library: bokeh
"""

import math

from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, LabelSet, Legend, LegendItem
from bokeh.plotting import figure


# Data - departmental budget allocation
categories = ["Engineering", "Marketing", "Operations", "Sales", "HR", "R&D"]
values = [35, 20, 15, 15, 8, 7]

# Calculate percentages and angles
total = sum(values)
percentages = [v / total * 100 for v in values]

# Calculate start and end angles for each wedge (in radians, counterclockwise from 3 o'clock)
angles = [v / total * 2 * math.pi for v in values]
start_angles = []
end_angles = []
cumulative = math.pi / 2  # Start from top (12 o'clock)

for angle in angles:
    start_angles.append(cumulative)
    cumulative -= angle  # Go clockwise
    end_angles.append(cumulative)

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Calculate label positions (middle of each wedge)
outer_radius = 0.9
inner_radius = 0.5  # ~55% of outer for donut appearance
label_radius = (outer_radius + inner_radius) / 2 + 0.05

label_x = []
label_y = []
for start, end in zip(start_angles, end_angles, strict=True):
    mid_angle = (start + end) / 2
    label_x.append(label_radius * math.cos(mid_angle))
    label_y.append(label_radius * math.sin(mid_angle))

# Create labels with percentages
labels = [f"{p:.1f}%" for p in percentages]


# Function to create wedge patch coordinates
def create_annular_wedge_patch(start_angle, end_angle, inner_r, outer_r, num_points=50):
    """Create x, y coordinates for an annular wedge as a polygon."""
    # Outer arc (from start to end)
    outer_angles = [start_angle + (end_angle - start_angle) * i / num_points for i in range(num_points + 1)]
    outer_x = [outer_r * math.cos(a) for a in outer_angles]
    outer_y = [outer_r * math.sin(a) for a in outer_angles]

    # Inner arc (from end back to start)
    inner_angles = [end_angle + (start_angle - end_angle) * i / num_points for i in range(num_points + 1)]
    inner_x = [inner_r * math.cos(a) for a in inner_angles]
    inner_y = [inner_r * math.sin(a) for a in inner_angles]

    # Combine to create closed polygon
    x = outer_x + inner_x
    y = outer_y + inner_y
    return x, y


# Create figure - hide axes for pie/donut charts
p = figure(
    width=4800,
    height=2700,
    title="Departmental Budget Allocation",
    x_range=(-1.3, 1.8),
    y_range=(-1.2, 1.2),
    tools="",
    toolbar_location=None,
)

# Remove axes and grid for clean donut chart
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Title styling
p.title.text_font_size = "48pt"
p.title.align = "center"

# Draw each wedge as a patch polygon for reliable color rendering
renderers = []
for i in range(len(categories)):
    wedge_x, wedge_y = create_annular_wedge_patch(start_angles[i], end_angles[i], inner_radius, outer_radius)
    renderer = p.patch(x=wedge_x, y=wedge_y, fill_color=colors[i], line_color="white", line_width=3)
    renderers.append(renderer)

# Add percentage labels
label_source = ColumnDataSource(data={"x": label_x, "y": label_y, "text": labels})

label_set = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_font_size="36pt",
    text_font_style="bold",
    text_align="center",
    text_baseline="middle",
    text_color="white",
)
p.add_layout(label_set)

# Create legend with renderers
legend_items = [LegendItem(label=cat, renderers=[renderers[i]]) for i, cat in enumerate(categories)]
legend = Legend(
    items=legend_items,
    location="center_right",
    label_text_font_size="32pt",
    glyph_height=40,
    glyph_width=40,
    spacing=15,
)
legend.border_line_color = None
legend.background_fill_alpha = 0
p.add_layout(legend, "right")

# Save as PNG and HTML
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
