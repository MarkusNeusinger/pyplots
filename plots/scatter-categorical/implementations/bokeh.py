"""pyplots.ai
scatter-categorical: Categorical Scatter Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure


# Data
np.random.seed(42)

# Generate three distinct groups with different patterns
n_per_group = 50

# Group A: Lower left cluster
x_a = np.random.normal(25, 5, n_per_group)
y_a = np.random.normal(30, 6, n_per_group)
cat_a = ["Product A"] * n_per_group

# Group B: Upper middle cluster
x_b = np.random.normal(50, 7, n_per_group)
y_b = np.random.normal(70, 8, n_per_group)
cat_b = ["Product B"] * n_per_group

# Group C: Right side, moderate y
x_c = np.random.normal(75, 6, n_per_group)
y_c = np.random.normal(50, 7, n_per_group)
cat_c = ["Product C"] * n_per_group

# Combine data
x = np.concatenate([x_a, x_b, x_c])
y = np.concatenate([y_a, y_b, y_c])
categories = cat_a + cat_b + cat_c

# Define colors for each category (Python Blue, Python Yellow, colorblind-safe red)
color_map = {"Product A": "#306998", "Product B": "#FFD43B", "Product C": "#E74C3C"}

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="scatter-categorical · bokeh · pyplots.ai",
    x_axis_label="Marketing Spend ($K)",
    y_axis_label="Customer Engagement Score",
)

# Plot each category separately for legend
legend_items = []

for cat, color in color_map.items():
    cat_source = ColumnDataSource(
        data={
            "x": [x[i] for i in range(len(x)) if categories[i] == cat],
            "y": [y[i] for i in range(len(y)) if categories[i] == cat],
        }
    )
    r = p.scatter(x="x", y="y", source=cat_source, size=30, color=color, alpha=0.7)
    legend_items.append((cat, [r]))

# Add legend
legend = Legend(items=legend_items, location="top_right")
legend.label_text_font_size = "36pt"
legend.glyph_height = 50
legend.glyph_width = 50
legend.spacing = 15
legend.padding = 20
p.add_layout(legend)

# Title styling
p.title.text_font_size = "48pt"
p.title.text_font_style = "bold"

# Axis label styling
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"

# Tick label styling
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#fafafa"

# Axis styling
p.axis.axis_line_width = 2
p.axis.major_tick_line_width = 2

# Save
export_png(p, filename="plot.png")
