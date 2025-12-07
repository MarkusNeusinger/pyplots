"""
box-basic: Basic Box Plot
Library: bokeh
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, FixedTicker, Whisker
from bokeh.palettes import Category10_4
from bokeh.plotting import figure


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Calculate box plot statistics for each group
group_names = sorted(data["group"].unique())
n_groups = len(group_names)

stats = {"x": [], "q1": [], "q2": [], "q3": [], "upper": [], "lower": []}
outliers = {"x": [], "y": []}

for i, group in enumerate(group_names):
    group_data = data[data["group"] == group]["value"].dropna()

    q1 = group_data.quantile(0.25)
    q2 = group_data.quantile(0.50)
    q3 = group_data.quantile(0.75)
    iqr = q3 - q1

    upper_fence = q3 + 1.5 * iqr
    lower_fence = q1 - 1.5 * iqr
    upper = group_data[group_data <= upper_fence].max()
    lower = group_data[group_data >= lower_fence].min()

    stats["x"].append(i)
    stats["q1"].append(q1)
    stats["q2"].append(q2)
    stats["q3"].append(q3)
    stats["upper"].append(upper)
    stats["lower"].append(lower)

    # Find outliers
    outlier_data = group_data[(group_data < lower_fence) | (group_data > upper_fence)]
    for val in outlier_data:
        outliers["x"].append(i)
        outliers["y"].append(val)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Basic Box Plot",
    x_axis_label="Group",
    y_axis_label="Value",
    toolbar_location="above",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

source = ColumnDataSource(data=stats)
box_width = 0.5
colors = Category10_4

# Draw boxes (Q1 to Q3)
for i, color in enumerate(colors):
    p.vbar(
        x=i,
        width=box_width,
        bottom=stats["q1"][i],
        top=stats["q3"][i],
        fill_color=color,
        fill_alpha=0.7,
        line_color="#333333",
        line_width=2,
    )

# Draw median lines
for i in range(n_groups):
    p.segment(
        x0=i - box_width / 2,
        y0=stats["q2"][i],
        x1=i + box_width / 2,
        y1=stats["q2"][i],
        line_color="#333333",
        line_width=3,
    )

# Draw whiskers
upper_whisker = Whisker(base="x", upper="upper", lower="q3", source=source, line_color="#333333", line_width=2)
upper_whisker.upper_head.size = 20
upper_whisker.upper_head.line_width = 2
upper_whisker.lower_head.size = 0
p.add_layout(upper_whisker)

lower_whisker = Whisker(base="x", upper="q1", lower="lower", source=source, line_color="#333333", line_width=2)
lower_whisker.upper_head.size = 0
lower_whisker.lower_head.size = 20
lower_whisker.lower_head.line_width = 2
p.add_layout(lower_whisker)

# Draw outliers
if outliers["x"]:
    outlier_source = ColumnDataSource(data=outliers)
    p.scatter(
        x="x", y="y", source=outlier_source, size=12, color="#DC2626", alpha=0.7, line_color="#333333", line_width=1
    )

# Set x-axis to show group names
p.xaxis.ticker = FixedTicker(ticks=list(range(n_groups)))
p.xaxis.major_label_overrides = dict(enumerate(group_names))

# Styling
p.title.text_font_size = "20pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.ygrid.grid_line_alpha = 0.3
p.xgrid.visible = False

# Save
export_png(p, filename="plot.png")
