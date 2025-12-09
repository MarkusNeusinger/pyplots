"""
pie-basic: Basic Pie Chart
Library: bokeh
"""

import math

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label, Legend, LegendItem
from bokeh.plotting import figure


# PyPlots.ai style colors
COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]

# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Calculate angles for pie slices
total = data["value"].sum()
data["angle"] = data["value"] / total * 2 * math.pi
data["percentage"] = data["value"] / total * 100

# Calculate cumulative angles for wedge positioning
data["end_angle"] = data["angle"].cumsum()
data["start_angle"] = data["end_angle"] - data["angle"]

# Apply start angle offset (start from top, 90 degrees)
start_rad = math.radians(90 - 90)  # Adjust for Bokeh coordinate system
data["start_angle"] = data["start_angle"] + start_rad
data["end_angle"] = data["end_angle"] + start_rad

# Assign colors (cycle if more categories than colors)
data["color"] = [COLORS[i % len(COLORS)] for i in range(len(data))]

# Create ColumnDataSource
source = ColumnDataSource(data)

# Create figure - 4800 x 2700 px as per style guide
p = figure(
    width=4800,
    height=2700,
    title="Market Share Distribution",
    tools="hover",
    tooltips=[("Category", "@category"), ("Value", "@value"), ("Percentage", "@percentage{0.1}%")],
    x_range=(-1.2, 2.0),
    y_range=(-1.2, 1.2),
)

# Draw wedges (pie slices)
renderers = p.wedge(
    x=0,
    y=0,
    radius=0.9,
    start_angle="start_angle",
    end_angle="end_angle",
    line_color="white",
    line_width=2,
    fill_color="color",
    source=source,
)

# Add percentage labels inside slices
for _, row in data.iterrows():
    mid_angle = (row["start_angle"] + row["end_angle"]) / 2
    label_radius = 0.55

    x = label_radius * math.cos(mid_angle)
    y = label_radius * math.sin(mid_angle)

    # Only show label if slice is large enough
    if row["percentage"] >= 5:
        label = Label(
            x=x,
            y=y,
            text=f"{row['percentage']:.1f}%",
            text_font_size="48pt",
            text_align="center",
            text_baseline="middle",
            text_color="white" if row["percentage"] >= 10 else "black",
        )
        p.add_layout(label)

# Create legend
legend_items = []
for i, cat in enumerate(data["category"]):
    legend_items.append(LegendItem(label=str(cat), renderers=[renderers], index=i))

leg = Legend(
    items=legend_items,
    location="center",
    label_text_font_size="48pt",
    background_fill_color="white",
    background_fill_alpha=1.0,
    border_line_color="black",
    border_line_width=1,
)
p.add_layout(leg, "right")

# Style configuration
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Title styling
p.title.text_font_size = "60pt"
p.title.align = "center"

# Background
p.background_fill_color = "white"

# Save
export_png(p, filename="plot.png")
