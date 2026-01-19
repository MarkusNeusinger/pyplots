""" pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, LabelSet, Range1d
from bokeh.plotting import figure


# Data - simulating a snapshot of live service metrics
np.random.seed(42)
categories = ["API Gateway", "Auth Service", "Database", "Cache", "Storage", "Queue"]
# Current values (shown with solid bars)
current_values = np.array([847, 623, 512, 891, 445, 678])
# Previous values (shown with ghosted effect to suggest motion)
previous_values = current_values * (0.85 + 0.3 * np.random.rand(len(categories)))
# Calculate changes
changes = current_values - previous_values

# Colors - Python Blue as primary, lighter shade for ghost effect
primary_color = "#306998"
ghost_color = "#306998"
ghost_alpha = 0.25

# Create figure with categorical x-axis
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="bar-realtime · bokeh · pyplots.ai",
    x_axis_label="Service",
    y_axis_label="Active Connections",
    toolbar_location=None,
)

# Create data sources
ghost_source = ColumnDataSource(data={"x": categories, "top": previous_values})

current_source = ColumnDataSource(
    data={
        "x": categories,
        "top": current_values,
        "value_text": [str(int(v)) for v in current_values],
        "label_y": current_values + 30,
        "change_text": [f"+{int(c)}" if c >= 0 else str(int(c)) for c in changes],
        "change_y": current_values + 80,
        "change_color": ["#2E7D32" if c >= 0 else "#C62828" for c in changes],
    }
)

# Plot ghosted previous values (suggesting motion/transition)
p.vbar(
    x="x",
    top="top",
    source=ghost_source,
    width=0.7,
    fill_color=ghost_color,
    fill_alpha=ghost_alpha,
    line_color=ghost_color,
    line_alpha=ghost_alpha,
    line_width=2,
)

# Plot current values
p.vbar(
    x="x",
    top="top",
    source=current_source,
    width=0.5,
    fill_color=primary_color,
    fill_alpha=0.85,
    line_color=primary_color,
    line_width=2,
)

# Add value labels above bars using LabelSet
value_labels = LabelSet(
    x="x",
    y="label_y",
    text="value_text",
    source=current_source,
    text_align="center",
    text_font_size="22pt",
    text_color="#333333",
)
p.add_layout(value_labels)

# Add change indicator labels
change_labels = LabelSet(
    x="x",
    y="change_y",
    text="change_text",
    source=current_source,
    text_align="center",
    text_font_size="18pt",
    text_color="change_color",
)
p.add_layout(change_labels)

# Styling
p.title.text_font_size = "32pt"
p.title.text_color = "#333333"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "20pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.major_label_orientation = 0.3

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Axis styling
p.y_range = Range1d(0, max(max(current_values), max(previous_values)) * 1.2)
p.outline_line_color = None
p.xaxis.axis_line_color = "#666666"
p.yaxis.axis_line_color = "#666666"

# Background
p.background_fill_color = "#FAFAFA"
p.border_fill_color = "#FFFFFF"

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="bar-realtime · bokeh · pyplots.ai")
