"""pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-10
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    facet_grid,
    geom_bar,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
)
from sklearn.datasets import load_iris


# Data: Iris dataset for multivariate analysis
np.random.seed(42)
iris = load_iris()
df = pd.DataFrame(iris.data, columns=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"])
df["Species"] = pd.Categorical([iris.target_names[i] for i in iris.target])

# Variables for the matrix (with units in labels)
variables = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
var_labels = [f"{v} (cm)" for v in variables]

# Colorblind-safe palette (Dark2 inspired - teal, orange, purple)
colors = ["#1B9E77", "#D95F02", "#7570B3"]

# Create long-form data for all cells
# For off-diagonal: scatter points with x and y
# For diagonal: histogram bars computed as binned counts
all_data = []

for i, var_y in enumerate(variables):
    for j, var_x in enumerate(variables):
        var_x_label = var_labels[j]
        var_y_label = var_labels[i]

        if i == j:
            # Diagonal: Create histogram data as bar chart data
            # Bin the data and create counts per species
            values = df[var_x]
            bins = np.linspace(values.min(), values.max(), 13)
            bin_centers = (bins[:-1] + bins[1:]) / 2
            bin_width = bins[1] - bins[0]

            for species in df["Species"].unique():
                species_vals = df[df["Species"] == species][var_x]
                counts, _ = np.histogram(species_vals, bins=bins)
                for k, count in enumerate(counts):
                    if count > 0:
                        all_data.append(
                            {
                                "x": bin_centers[k],
                                "y": count,
                                "Species": species,
                                "var_x": var_x_label,
                                "var_y": var_y_label,
                                "cell_type": "histogram",
                            }
                        )
        else:
            # Off-diagonal: scatter data
            for _, row in df.iterrows():
                all_data.append(
                    {
                        "x": row[var_x],
                        "y": row[var_y],
                        "Species": row["Species"],
                        "var_x": var_x_label,
                        "var_y": var_y_label,
                        "cell_type": "scatter",
                    }
                )

plot_df = pd.DataFrame(all_data)

# Set factor levels for proper ordering
plot_df["var_x"] = pd.Categorical(plot_df["var_x"], categories=var_labels, ordered=True)
plot_df["var_y"] = pd.Categorical(plot_df["var_y"], categories=var_labels[::-1], ordered=True)

# Split data for different geoms
scatter_df = plot_df[plot_df["cell_type"] == "scatter"].copy()
hist_df = plot_df[plot_df["cell_type"] == "histogram"].copy()

# Compute bin width for histogram bars
bin_width = (df[variables[0]].max() - df[variables[0]].min()) / 12 * 0.9

# Create scatter plot matrix with histograms on diagonal
# Use geom_bar with stat="identity" for pre-computed histogram data
plot = (
    ggplot(mapping=aes(x="x", y="y"))
    + geom_point(data=scatter_df, mapping=aes(color="Species"), size=3.5, alpha=0.7)
    + geom_bar(
        data=hist_df, mapping=aes(fill="Species"), stat="identity", width=bin_width, alpha=0.7, position="identity"
    )
    + facet_grid("var_y ~ var_x", scales="free")
    + scale_color_manual(values=colors)
    + scale_fill_manual(values=colors)
    + labs(
        title="scatter-matrix-interactive · plotnine · pyplots.ai",
        subtitle="Iris Dataset: Pairwise Scatter Plots with Univariate Distributions\n(Note: Interactive brushing requires Plotly/Bokeh/Altair)",
        x="",
        y="",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 16),
        plot_title=element_text(size=24, weight="bold", ha="left"),
        plot_subtitle=element_text(size=14, color="#666666"),
        strip_text_x=element_text(size=14),
        strip_text_y=element_text(size=14, angle=0),
        axis_text=element_text(size=11),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="bottom",
        legend_background=element_rect(fill="white", alpha=0.9),
        panel_spacing=0.03,
        panel_grid_major=element_line(color="#cccccc", alpha=0.3),
        panel_grid_minor=element_line(color="#eeeeee", alpha=0.2),
        panel_background=element_rect(fill="white"),
    )
)

# Save plot
plot.save("plot.png", dpi=300, width=16, height=16, verbose=False)
