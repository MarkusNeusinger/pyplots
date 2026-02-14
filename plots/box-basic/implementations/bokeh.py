""" pyplots.ai
box-basic: Basic Box Plot
Library: bokeh 3.8.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Whisker
from bokeh.plotting import figure
from bokeh.transform import factor_cmap


# Data - Test scores across 4 classes with varying distributions
np.random.seed(42)
categories = ["Class A", "Class B", "Class C", "Class D"]

scores = {
    "Class A": np.random.normal(75, 10, 100),
    "Class B": np.concatenate([np.random.normal(85, 5, 90), np.array([45, 50, 52])]),
    "Class C": np.random.normal(68, 18, 100),
    "Class D": np.concatenate([np.random.normal(78, 8, 95), np.array([105, 108, 42, 40])]),
}

# Box plot statistics
colors = ["#306998", "#4B8BBE", "#E5A03A", "#7A9E3D"]

box_data = {"cat": [], "q1": [], "q2": [], "q3": [], "upper": [], "lower": [], "iqr": []}
outlier_x = []
outlier_y = []

for cat in categories:
    values = np.array(scores[cat])
    q1 = np.percentile(values, 25)
    q2 = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    lower_fence = q1 - 1.5 * iqr
    upper_whisker = values[values <= upper_fence].max()
    lower_whisker = values[values >= lower_fence].min()

    box_data["cat"].append(cat)
    box_data["q1"].append(round(q1, 1))
    box_data["q2"].append(round(q2, 1))
    box_data["q3"].append(round(q3, 1))
    box_data["upper"].append(round(upper_whisker, 1))
    box_data["lower"].append(round(lower_whisker, 1))
    box_data["iqr"].append(round(iqr, 1))

    outliers = values[(values < lower_fence) | (values > upper_fence)]
    for o in outliers:
        outlier_x.append(cat)
        outlier_y.append(round(o, 1))

source = ColumnDataSource(data=box_data)

# Figure (4800 x 2700 px)
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="box-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Class",
    y_axis_label="Test Score (points)",
    toolbar_location=None,
    tools="",
)

# Boxes (q1 to q3) with factor_cmap
cmap = factor_cmap("cat", palette=colors, factors=categories)

box_upper = p.vbar(
    x="cat",
    top="q3",
    bottom="q2",
    source=source,
    width=0.5,
    fill_color=cmap,
    line_color="#333333",
    line_width=2,
    fill_alpha=0.85,
)
box_lower = p.vbar(
    x="cat",
    top="q2",
    bottom="q1",
    source=source,
    width=0.5,
    fill_color=cmap,
    line_color="#333333",
    line_width=2,
    fill_alpha=0.85,
)

# Median lines
median_source = ColumnDataSource(data={"x": box_data["cat"], "y": box_data["q2"]})
p.rect(x="x", y="y", width=0.5, height=0.5, source=median_source, fill_color="#1a1a1a", line_color="#1a1a1a")

# Whiskers
whisker = Whisker(
    base="cat", upper="upper", lower="lower", source=source, level="annotation", line_width=3, line_color="#333333"
)
whisker.upper_head.size = 35
whisker.lower_head.size = 35
whisker.upper_head.line_width = 3
whisker.lower_head.line_width = 3
p.add_layout(whisker)

# Outliers
if outlier_x:
    outlier_source = ColumnDataSource(data={"x": outlier_x, "y": outlier_y})
    p.scatter(
        x="x",
        y="y",
        source=outlier_source,
        size=18,
        fill_color="white",
        line_color="#333333",
        line_width=2.5,
        marker="circle",
        alpha=0.9,
    )

# Hover tool on boxes - Bokeh distinctive interactive feature
hover = HoverTool(
    renderers=[box_upper, box_lower],
    tooltips=[
        ("Class", "@cat"),
        ("Median", "@q2{0.1}"),
        ("Q1", "@q1{0.1}"),
        ("Q3", "@q3{0.1}"),
        ("IQR", "@iqr{0.1}"),
        ("Whisker range", "@lower{0.1} \u2013 @upper{0.1}"),
    ],
)
p.add_tools(hover)

# Styling for 4800x2700 px
p.title.text_font_size = "36pt"
p.title.text_font_style = "normal"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Grid
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_width = 1

# Spines - remove top and right
p.outline_line_color = None
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.major_tick_line_color = None
p.yaxis.major_tick_line_color = None

# Background
p.background_fill_color = None
p.border_fill_color = None

# Save
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
