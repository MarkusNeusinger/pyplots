""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Product quality ratings across different product lines
np.random.seed(42)
categories = ["Electronics", "Furniture", "Clothing", "Sports", "Home & Garden"]
n_points_per_cat = 25

data = {"category": [], "value": [], "x_jitter": []}
for i, cat in enumerate(categories):
    # Different distributions for each category
    if cat == "Electronics":
        values = np.random.normal(85, 8, n_points_per_cat)
    elif cat == "Furniture":
        values = np.random.normal(72, 12, n_points_per_cat)
    elif cat == "Clothing":
        values = np.random.normal(78, 10, n_points_per_cat)
    elif cat == "Sports":
        values = np.random.normal(88, 6, n_points_per_cat)
    else:  # Home & Garden
        values = np.random.normal(65, 15, n_points_per_cat)

    # Add jitter for strip plot effect
    jitter = np.random.uniform(-0.25, 0.25, n_points_per_cat)

    data["category"].extend([cat] * n_points_per_cat)
    data["value"].extend(values.clip(0, 100))  # Clip to valid range
    data["x_jitter"].extend([i + j for j in jitter])

source = ColumnDataSource(data)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="cat-strip · bokeh · pyplots.ai",
    x_axis_label="Product Line",
    y_axis_label="Quality Rating (0-100)",
    x_range=(-0.5, len(categories) - 0.5),
    y_range=(0, 105),
)

# Plot points with jitter
p.scatter(
    x="x_jitter", y="value", source=source, size=25, color="#306998", alpha=0.7, line_color="#1a3a57", line_width=2
)

# Style the plot - scaled for 4800x2700 canvas
p.title.text_font_size = "48pt"
p.title.align = "center"

p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Set category labels on x-axis
p.xaxis.ticker = list(range(len(categories)))
p.xaxis.major_label_overrides = dict(enumerate(categories))

# Axis styling
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#fafafa"

# Save
export_png(p, filename="plot.png")
