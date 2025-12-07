"""
scatter-color-groups: Scatter Plot with Color Groups
Library: bokeh
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Iris-like dataset
np.random.seed(42)
n_per_group = 50

data = pd.DataFrame({
    "sepal_length": np.concatenate([
        np.random.normal(5.0, 0.35, n_per_group),
        np.random.normal(5.9, 0.50, n_per_group),
        np.random.normal(6.6, 0.60, n_per_group),
    ]),
    "sepal_width": np.concatenate([
        np.random.normal(3.4, 0.38, n_per_group),
        np.random.normal(2.8, 0.30, n_per_group),
        np.random.normal(3.0, 0.30, n_per_group),
    ]),
    "species": ["setosa"] * n_per_group + ["versicolor"] * n_per_group + ["virginica"] * n_per_group,
})

# Color palette (from style guide)
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]
species_list = data["species"].unique().tolist()
color_map = {species: colors[i] for i, species in enumerate(species_list)}
data["color"] = data["species"].map(color_map)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Scatter Plot with Color Groups",
    x_axis_label="Sepal Length (cm)",
    y_axis_label="Sepal Width (cm)",
)

# Plot each group separately for legend
for species in species_list:
    species_data = data[data["species"] == species]
    source = ColumnDataSource(data={"x": species_data["sepal_length"], "y": species_data["sepal_width"]})
    p.scatter(
        x="x", y="y", source=source, size=12, alpha=0.7, color=color_map[species], legend_label=species.capitalize()
    )

# Styling
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.legend.label_text_font_size = "16pt"
p.legend.location = "top_right"
p.grid.grid_line_alpha = 0.3

# Save
export_png(p, filename="plot.png")
