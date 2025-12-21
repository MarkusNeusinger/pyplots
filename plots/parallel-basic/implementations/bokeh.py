""" pyplots.ai
parallel-basic: Basic Parallel Coordinates Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import pandas as pd
from bokeh.io import export_png, save
from bokeh.models import Legend, LegendItem
from bokeh.plotting import figure


# Data - Iris dataset for multivariate demonstration
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

# Define numeric columns and normalize to [0, 1] for fair comparison
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
df_norm = df.copy()
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    df_norm[col] = (df[col] - min_val) / (max_val - min_val)

# Create figure (4800x2700 px)
p = figure(
    width=4800,
    height=2700,
    title="parallel-basic · bokeh · pyplots.ai",
    x_axis_label="Dimension",
    y_axis_label="Normalized Value",
    x_range=(-0.3, 3.3),
    y_range=(-0.05, 1.10),
)

# Styling for 4800x2700 px canvas
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Define colors for species
colors = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#4CAF50"}

# X positions for each dimension
x_coords = list(range(len(numeric_cols)))

# Track renderers for legend
legend_items = []
renderers_by_species = {}

# Plot parallel coordinates - each line connects values across axes
for _, row in df_norm.iterrows():
    species = row["species"]
    y_coords = [row[col] for col in numeric_cols]
    renderer = p.line(x_coords, y_coords, line_color=colors[species], line_alpha=0.5, line_width=2)
    # Keep one renderer per species for legend
    if species not in renderers_by_species:
        renderers_by_species[species] = renderer

# Create legend
for species_name in ["setosa", "versicolor", "virginica"]:
    legend_items.append(LegendItem(label=species_name.capitalize(), renderers=[renderers_by_species[species_name]]))

legend = Legend(items=legend_items, location="top_right")
legend.label_text_font_size = "18pt"
legend.title = "Species"
legend.title_text_font_size = "20pt"
p.add_layout(legend)

# Custom x-axis labels with original scale ranges
axis_labels = [
    f"Sepal Length\n({df['sepal_length'].min():.1f}-{df['sepal_length'].max():.1f} cm)",
    f"Sepal Width\n({df['sepal_width'].min():.1f}-{df['sepal_width'].max():.1f} cm)",
    f"Petal Length\n({df['petal_length'].min():.1f}-{df['petal_length'].max():.1f} cm)",
    f"Petal Width\n({df['petal_width'].min():.1f}-{df['petal_width'].max():.1f} cm)",
]
p.xaxis.ticker = x_coords
p.xaxis.major_label_overrides = dict(enumerate(axis_labels))

# Grid styling - subtle
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = [6, 4]

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="parallel-basic · bokeh · pyplots.ai")
