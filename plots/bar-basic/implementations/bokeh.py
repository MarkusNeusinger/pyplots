"""
bar-basic: Basic Bar Chart
Library: bokeh
"""

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure, output_file, save


# Data - Product sales by category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [42500, 31200, 28700, 19800, 15400, 12600]

# Create ColumnDataSource
source = ColumnDataSource(data={"categories": categories, "values": values})

# Create figure with categorical x-axis (4800 × 2700 px)
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="bar-basic · bokeh · pyplots.ai",
    x_axis_label="Product Category",
    y_axis_label="Sales ($)",
    toolbar_location=None,
)

# Create bars
p.vbar(x="categories", top="values", source=source, width=0.7, color="#306998", alpha=0.9)

# Add value labels on top of bars
labels = LabelSet(
    x="categories",
    y="values",
    text="values",
    level="glyph",
    x_offset=-25,
    y_offset=5,
    source=source,
    text_font_size="28pt",
    text_color="#333333",
)
p.add_layout(labels)

# Styling for 4800×2700 px
p.title.text_font_size = "36pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "24pt"
p.yaxis.major_label_text_font_size = "24pt"

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Y-axis starts at 0
p.y_range.start = 0

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactivity
output_file("plot.html")
save(p)
