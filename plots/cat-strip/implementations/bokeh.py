"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import jitter


# Data - Product quality scores across manufacturing batches
np.random.seed(42)

categories = ["Batch A", "Batch B", "Batch C", "Batch D", "Batch E"]
n_per_category = 25

# Generate different distributions per category
data = {
    "Batch A": np.random.normal(85, 5, n_per_category),  # High quality, consistent
    "Batch B": np.random.normal(78, 8, n_per_category),  # Medium, more variable
    "Batch C": np.random.normal(92, 3, n_per_category),  # Very high, tight
    "Batch D": np.random.normal(70, 12, n_per_category),  # Lower, high variability
    "Batch E": np.random.normal(82, 6, n_per_category),  # Medium-high
}

# Prepare data
cat_list = []
value_list = []

for cat in categories:
    values = data[cat]
    n = len(values)
    cat_list.extend([cat] * n)
    value_list.extend(values)

# Create ColumnDataSource
source = ColumnDataSource(data={"category": cat_list, "value": value_list})

# Create figure with categorical x-axis
p = figure(
    width=4800,
    height=2700,
    x_range=categories,
    title="cat-strip · bokeh · pyplots.ai",
    x_axis_label="Manufacturing Batch",
    y_axis_label="Quality Score",
    tools="pan,box_zoom,reset,save",
    toolbar_location="right",
)

# Plot strip points with jitter using transform
p.scatter(
    x=jitter("category", width=0.5, range=p.x_range),
    y="value",
    source=source,
    size=25,
    alpha=0.7,
    color="#306998",
    line_color="#1a3a5c",
    line_width=2,
)

# Styling - Text sizes for 4800x2700 canvas (scaled up)
p.title.text_font_size = "48pt"
p.title.text_font_style = "bold"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Background and outline
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"
p.outline_line_color = "#cccccc"
p.outline_line_width = 2

# Axis styling
p.xaxis.major_tick_line_color = "#666666"
p.yaxis.major_tick_line_color = "#666666"
p.xaxis.axis_line_color = "#666666"
p.yaxis.axis_line_color = "#666666"
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2

# Save as PNG and HTML
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="cat-strip · bokeh · pyplots.ai")
