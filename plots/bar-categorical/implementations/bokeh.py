"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - simulate raw categorical data and count frequencies
np.random.seed(42)

# Simulate survey responses about preferred programming languages
categories = ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"]
weights = [0.30, 0.25, 0.15, 0.10, 0.08, 0.07, 0.05]

# Generate 500 raw category values (like raw survey data)
raw_data = np.random.choice(categories, size=500, p=weights)

# Count frequencies (this is what bar-categorical does)
unique, counts = np.unique(raw_data, return_counts=True)

# Sort by count descending for better visualization
sorted_indices = np.argsort(counts)[::-1]
sorted_categories = unique[sorted_indices].tolist()
sorted_counts = counts[sorted_indices].tolist()

# Create ColumnDataSource
source = ColumnDataSource(data={"categories": sorted_categories, "counts": sorted_counts})

# Create figure with categorical x-axis
p = figure(
    width=4800,
    height=2700,
    x_range=sorted_categories,
    title="bar-categorical · bokeh · pyplots.ai",
    x_axis_label="Programming Language",
    y_axis_label="Number of Responses",
    toolbar_location=None,
)

# Plot bars
p.vbar(
    x="categories",
    top="counts",
    source=source,
    width=0.7,
    color="#306998",
    alpha=0.85,
    line_color="#1e4a6e",
    line_width=3,
)

# Styling for large canvas (4800x2700 px) - scaled up ~3-4x
p.title.text_font_size = "48pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Axis styling
p.xaxis.major_label_orientation = 0.0  # Horizontal labels
p.y_range.start = 0
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "#ffffff"

# Outline
p.outline_line_color = "#cccccc"
p.outline_line_width = 1

# Add padding
p.min_border_left = 120
p.min_border_bottom = 100

# Save as PNG
export_png(p, filename="plot.png")
