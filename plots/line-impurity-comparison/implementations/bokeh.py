""" pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 84/100 | Created: 2026-02-17
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label, Legend
from bokeh.plotting import figure


# Data
p_vals = np.linspace(0, 1, 200)

# Gini impurity: 2 * p * (1 - p), already in [0, 1]
gini = 2 * p_vals * (1 - p_vals)

# Entropy: -p * log2(p) - (1-p) * log2(1-p), normalized to [0, 1]
with np.errstate(divide="ignore", invalid="ignore"):
    entropy = -p_vals * np.log2(p_vals) - (1 - p_vals) * np.log2(1 - p_vals)
entropy = np.nan_to_num(entropy, nan=0.0)

source_gini = ColumnDataSource(data={"p": p_vals, "impurity": gini})
source_entropy = ColumnDataSource(data={"p": p_vals, "impurity": entropy})

# Plot
fig = figure(
    width=4800,
    height=2700,
    title="line-impurity-comparison \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Probability (p)",
    y_axis_label="Impurity Measure",
    x_range=(-0.02, 1.02),
    y_range=(-0.05, 1.15),
)

# Lines
line_gini = fig.line(x="p", y="impurity", source=source_gini, line_width=7, line_color="#306998")
line_entropy = fig.line(
    x="p", y="impurity", source=source_entropy, line_width=7, line_color="#E24A33", line_dash=[14, 7]
)

# Annotate max points at p=0.5
fig.scatter(x=[0.5, 0.5], y=[0.5, 1.0], size=24, fill_color=["#306998", "#E24A33"], line_color="white", line_width=3)

# Connector line between the two max dots
fig.segment(x0=[0.5], y0=[0.5], x1=[0.5], y1=[1.0], line_color="#999999", line_width=2, line_dash="dotted")

max_label = Label(x=0.53, y=1.03, text="p = 0.5 (maximum impurity)", text_font_size="30pt", text_color="#555555")
fig.add_layout(max_label)

# Legend with formulas
legend = Legend(
    items=[
        ("Gini: 2p(1\u2212p)", [line_gini]),
        ("Entropy: \u2212p log\u2082p \u2212 (1\u2212p) log\u2082(1\u2212p)", [line_entropy]),
    ],
    location="top_left",
    label_text_font_size="30pt",
    glyph_width=70,
    glyph_height=35,
    spacing=18,
    padding=30,
    border_line_alpha=0,
    background_fill_alpha=0.8,
)
fig.add_layout(legend)

# Style - text sizes scaled for 4800x2700 canvas
fig.title.text_font_size = "42pt"
fig.xaxis.axis_label_text_font_size = "32pt"
fig.yaxis.axis_label_text_font_size = "32pt"
fig.xaxis.major_label_text_font_size = "24pt"
fig.yaxis.major_label_text_font_size = "24pt"

# Grid - y-axis only, subtle
fig.xgrid.grid_line_alpha = 0
fig.ygrid.grid_line_alpha = 0.2

# Background
fig.background_fill_color = "#fafafa"
fig.border_fill_color = "white"
fig.outline_line_color = None

# Axis styling
fig.axis.axis_line_width = 2
fig.axis.axis_line_color = "#333333"
fig.axis.minor_tick_line_color = None

# Remove toolbar for cleaner static image
fig.toolbar_location = None

# Save
export_png(fig, filename="plot.png")

output_file("plot.html")
save(fig)
