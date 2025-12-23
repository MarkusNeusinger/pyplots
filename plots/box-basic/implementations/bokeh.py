""" pyplots.ai
box-basic: Basic Box Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure


# Data - Test scores across 4 classes with varying distributions
np.random.seed(42)
categories = ["Class A", "Class B", "Class C", "Class D"]

# Create distributions with different characteristics to showcase box plot features
data = {
    "Class A": np.random.normal(75, 10, 100),  # Medium spread
    "Class B": np.concatenate([np.random.normal(85, 5, 90), np.array([45, 50, 52])]),  # Tight with low outliers
    "Class C": np.random.normal(68, 18, 100),  # Wide spread, likely outliers
    "Class D": np.concatenate([np.random.normal(78, 8, 95), np.array([105, 108, 42, 40])]),  # Outliers on both ends
}
colors = ["#306998", "#FFD43B", "#4B8BBE", "#646464"]

# Calculate box plot statistics for each category
box_data = {"cat": [], "q1": [], "q2": [], "q3": [], "upper": [], "lower": [], "color": []}
outlier_data = {"x": [], "y": []}

for i, cat in enumerate(categories):
    values = np.array(data[cat])
    q1 = np.percentile(values, 25)
    q2 = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    upper_whisker = min(values.max(), q3 + 1.5 * iqr)
    lower_whisker = max(values.min(), q1 - 1.5 * iqr)

    box_data["cat"].append(cat)
    box_data["q1"].append(q1)
    box_data["q2"].append(q2)
    box_data["q3"].append(q3)
    box_data["upper"].append(upper_whisker)
    box_data["lower"].append(lower_whisker)
    box_data["color"].append(colors[i])

    # Collect outliers
    outliers = values[(values < lower_whisker) | (values > upper_whisker)]
    for out in outliers:
        outlier_data["x"].append(cat)
        outlier_data["y"].append(out)

source = ColumnDataSource(data=box_data)

# Create figure with categorical x-axis (4800 x 2700 px)
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="box-basic · bokeh · pyplots.ai",
    x_axis_label="Class",
    y_axis_label="Test Score",
    toolbar_location=None,
)

# Draw boxes (from q1 to q3)
p.vbar(
    x="cat",
    top="q3",
    bottom="q1",
    source=source,
    width=0.5,
    fill_color="color",
    line_color="black",
    line_width=3,
    fill_alpha=0.8,
)

# Median lines - draw segment for each category
# Use ColumnDataSource with segment glyphs for categorical axis
median_segments = {
    "x": categories,  # categorical positions
    "y": box_data["q2"],
}
median_source = ColumnDataSource(data=median_segments)

# For categorical x-axis, use hbar with height=0 alternative: draw using rect
# Actually use rect with very small height to create a line effect
p.rect(
    x="x",
    y="y",
    width=0.5,
    height=1,  # Small height for line effect
    source=median_source,
    fill_color="black",
    line_color="black",
)

# Whiskers
whisker = Whisker(
    base="cat", upper="upper", lower="lower", source=source, level="annotation", line_width=3, line_color="black"
)
whisker.upper_head.size = 40
whisker.lower_head.size = 40
p.add_layout(whisker)

# Outliers
if len(outlier_data["x"]) > 0:
    outlier_source = ColumnDataSource(data=outlier_data)
    p.scatter(
        x="x",
        y="y",
        source=outlier_source,
        size=20,
        fill_color="white",
        line_color="black",
        line_width=3,
        marker="circle",
    )

# Styling for 4800x2700 px
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Background styling
p.background_fill_color = None
p.border_fill_color = None

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
