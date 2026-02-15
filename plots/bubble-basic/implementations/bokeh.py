""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label, Range1d
from bokeh.plotting import figure, output_file, save


# Data — City metrics: population density vs median income, bubble = green space per capita
np.random.seed(42)
n_cities = 40

population_density = np.random.uniform(500, 12000, n_cities)  # people per km²
median_income = 30 + population_density / 400 + np.random.normal(0, 4, n_cities)  # thousands USD
green_space = np.random.uniform(5, 60, n_cities)  # m² per capita

# Scale bubble sizes by area for accurate perception (spec requirement)
size_min, size_max = 25, 110
green_normalized = (green_space - green_space.min()) / (green_space.max() - green_space.min())
bubble_size = size_min + (size_max - size_min) * green_normalized

source = ColumnDataSource(data={"density": population_density, "income": median_income, "size": bubble_size})

# Plot
p = figure(
    width=4800,
    height=2700,
    title="bubble-basic · bokeh · pyplots.ai",
    x_axis_label="Population Density (people/km²)",
    y_axis_label="Median Income (thousands USD)",
    toolbar_location=None,
)

p.scatter(
    x="density",
    y="income",
    size="size",
    source=source,
    fill_color="#306998",
    fill_alpha=0.55,
    line_color="white",
    line_width=1.5,
)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "30pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Clean frame — remove outline and tick marks
p.outline_line_color = None
p.xaxis.axis_line_color = "#333333"
p.yaxis.axis_line_color = "#333333"
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.major_tick_line_color = None
p.yaxis.major_tick_line_color = None

# Subtle grid for scatter
p.xgrid.grid_line_alpha = 0.18
p.ygrid.grid_line_alpha = 0.18
p.xgrid.grid_line_color = "#999999"
p.ygrid.grid_line_color = "#999999"

# Size legend in bottom-right (empty due to positive correlation)
ref_sizes = [size_min, (size_min + size_max) / 2, size_max]
ref_labels = [
    f"{green_space.min():.0f} m²/capita",
    f"{(green_space.min() + green_space.max()) / 2:.0f} m²/capita",
    f"{green_space.max():.0f} m²/capita",
]

legend_x = 9200
legend_y_top = 36
legend_spacing = 3.5

p.add_layout(
    Label(
        x=legend_x - 400,
        y=legend_y_top + 3,
        text="Green Space",
        text_font_size="22pt",
        text_font_style="bold",
        text_color="#333333",
    )
)

for i, (sz, lbl) in enumerate(zip(ref_sizes, ref_labels, strict=True)):
    ly = legend_y_top - i * legend_spacing
    ref_src = ColumnDataSource(data={"x": [legend_x], "y": [ly], "size": [sz]})
    p.scatter(
        x="x",
        y="y",
        size="size",
        source=ref_src,
        fill_color="#306998",
        fill_alpha=0.55,
        line_color="white",
        line_width=1.5,
    )
    p.add_layout(
        Label(x=legend_x + 700, y=ly, text=lbl, text_font_size="18pt", text_baseline="middle", text_color="#444444")
    )

# Ranges — snug around data with minimal extension for legend
p.x_range = Range1d(start=-200, end=13000)
p.y_range = Range1d(start=25, end=67)

p.background_fill_color = None
p.border_fill_color = "white"

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
