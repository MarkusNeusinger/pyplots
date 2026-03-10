"""pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-03-10
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, CustomJSTickFormatter, FixedTicker, Label, Range1d
from bokeh.plotting import figure


# Data - Fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 28, 12]
icon_value = 5
colors = ["#306998", "#E8963E", "#F2C94C", "#7B68AE", "#5DA87E"]

# Build icon grid positions
full_x, full_y, full_c = [], [], []
bg_x, bg_y = [], []
wedge_x, wedge_y, wedge_c, wedge_end = [], [], [], []
n_cats = len(categories)
radius = 0.36

for i, (_cat, val, color) in enumerate(zip(categories, values, colors, strict=True)):
    n_full = int(val // icon_value)
    remainder = val % icon_value
    fraction = remainder / icon_value
    y = n_cats - 1 - i

    for j in range(n_full):
        full_x.append(j)
        full_y.append(y)
        full_c.append(color)

    if fraction > 0:
        bg_x.append(n_full)
        bg_y.append(y)
        wedge_x.append(n_full)
        wedge_y.append(y)
        wedge_c.append(color)
        wedge_end.append(np.pi / 2 - fraction * 2 * np.pi)

# Figure
max_icons = max(int(np.ceil(v / icon_value)) for v in values)
p = figure(
    width=4800,
    height=2700,
    x_range=Range1d(-0.8, max_icons + 0.5),
    y_range=Range1d(-1.0, n_cats - 0.2),
    toolbar_location=None,
    title="Fruit Production · pictogram-basic · bokeh · pyplots.ai",
)

# Full icons
full_source = ColumnDataSource(data={"x": full_x, "y": full_y, "color": full_c})
p.circle(x="x", y="y", radius=radius, source=full_source, color="color", alpha=0.9, line_color="white", line_width=2)

# Partial icon backgrounds (gray circles)
if bg_x:
    bg_source = ColumnDataSource(data={"x": bg_x, "y": bg_y})
    p.circle(
        x="x", y="y", radius=radius, source=bg_source, color="#E0E0E0", alpha=0.4, line_color="white", line_width=2
    )

    # Partial icon fills (wedges)
    wedge_source = ColumnDataSource(data={"x": wedge_x, "y": wedge_y, "color": wedge_c, "end_angle": wedge_end})
    p.wedge(
        x="x",
        y="y",
        radius=radius,
        start_angle=np.pi / 2,
        end_angle="end_angle",
        direction="clock",
        source=wedge_source,
        color="color",
        alpha=0.9,
        line_color="white",
        line_width=2,
    )

# Legend annotation
legend_label = Label(
    x=0,
    y=-0.7,
    text="Each ● = 5,000 tonnes",
    text_font_size="22pt",
    text_color="#555555",
    x_units="data",
    y_units="data",
)
p.add_layout(legend_label)

# Style
p.title.text_font_size = "36pt"
p.title.align = "center"

# Y-axis: category labels
cat_labels = [categories[n_cats - 1 - i] for i in range(n_cats)]
p.yaxis.ticker = FixedTicker(ticks=list(range(n_cats)))
p.yaxis.formatter = CustomJSTickFormatter(args={"labels": cat_labels}, code="return labels[tick] || '';")
p.yaxis.major_label_text_font_size = "24pt"

# X-axis: hide
p.xaxis.visible = False

# Remove spines and grid
p.outline_line_color = None
p.grid.grid_line_color = None
p.xaxis.axis_line_color = None
p.yaxis.axis_line_color = None
p.yaxis.major_tick_line_color = None
p.yaxis.minor_tick_line_color = None

# Background
p.background_fill_color = "#FFFFFF"
p.border_fill_color = "#FFFFFF"

# Padding
p.min_border_left = 200
p.min_border_bottom = 100

# Save
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
