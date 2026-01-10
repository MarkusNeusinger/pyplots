# ruff: noqa: F405
"""pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-10
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()

# Data - Synthetic iris-like dataset (4 numeric variables, 150 points)
np.random.seed(42)

# Generate measurements for three plant species with realistic correlations
n_per_species = 50

# Species A (small flowers): lower values
species_a = pd.DataFrame(
    {
        "Sepal Length (cm)": np.random.normal(5.0, 0.35, n_per_species),
        "Sepal Width (cm)": np.random.normal(3.4, 0.38, n_per_species),
        "Petal Length (cm)": np.random.normal(1.5, 0.17, n_per_species),
        "Petal Width (cm)": np.random.normal(0.25, 0.10, n_per_species),
        "Species": "Setosa",
    }
)

# Species B (medium flowers): intermediate values with correlation
base_b = np.random.normal(0, 1, n_per_species)
species_b = pd.DataFrame(
    {
        "Sepal Length (cm)": 5.9 + 0.5 * base_b + np.random.normal(0, 0.2, n_per_species),
        "Sepal Width (cm)": 2.8 + 0.3 * base_b + np.random.normal(0, 0.2, n_per_species),
        "Petal Length (cm)": 4.3 + 0.5 * base_b + np.random.normal(0, 0.3, n_per_species),
        "Petal Width (cm)": 1.3 + 0.2 * base_b + np.random.normal(0, 0.15, n_per_species),
        "Species": "Versicolor",
    }
)

# Species C (large flowers): higher values with strong correlation
base_c = np.random.normal(0, 1, n_per_species)
species_c = pd.DataFrame(
    {
        "Sepal Length (cm)": 6.6 + 0.6 * base_c + np.random.normal(0, 0.3, n_per_species),
        "Sepal Width (cm)": 3.0 + 0.3 * base_c + np.random.normal(0, 0.25, n_per_species),
        "Petal Length (cm)": 5.6 + 0.6 * base_c + np.random.normal(0, 0.3, n_per_species),
        "Petal Width (cm)": 2.0 + 0.3 * base_c + np.random.normal(0, 0.2, n_per_species),
        "Species": "Virginica",
    }
)

df = pd.concat([species_a, species_b, species_c], ignore_index=True)

# Variables for the scatter matrix
variables = ["Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"]
n = len(variables)

# Color palette
colors = ["#306998", "#FFD43B", "#DC2626"]

# Create individual plots for the 4x4 matrix
plots = []
for i, var_y in enumerate(variables):
    for j, var_x in enumerate(variables):
        if i == j:
            # Diagonal: histogram showing distribution
            p = (
                ggplot(df, aes(x=var_x, fill="Species"))
                + geom_histogram(alpha=0.7, bins=15, position="identity")
                + scale_fill_manual(values=colors)
                + theme_minimal()
                + theme(
                    axis_title=element_blank(),
                    axis_text=element_text(size=10),
                    legend_position="none",
                    plot_margin=[0, 0, 0, 0],
                )
            )
        else:
            # Off-diagonal: scatter plot with tooltips for interactivity
            p = (
                ggplot(df, aes(x=var_x, y=var_y, color="Species", fill="Species"))
                + geom_point(
                    size=3,
                    alpha=0.7,
                    shape=21,
                    tooltips=layer_tooltips()
                    .line("Species: @Species")
                    .format("@{" + var_x + "}", ".2f")
                    .format("@{" + var_y + "}", ".2f"),
                )
                + scale_color_manual(values=colors)
                + scale_fill_manual(values=colors)
                + theme_minimal()
                + theme(
                    axis_title=element_blank(),
                    axis_text=element_text(size=10),
                    legend_position="none",
                    plot_margin=[0, 0, 0, 0],
                )
            )
        plots.append(p)

# Calculate regions for ggbunch (4x4 grid)
# Leave space for title at top and legend at bottom
title_height = 0.08
legend_height = 0.08
grid_height = 1 - title_height - legend_height
cell_width = 1.0 / n
cell_height = grid_height / n

regions = []
for idx in range(n * n):
    row = idx // n
    col = idx % n
    x = col * cell_width
    y = title_height + row * cell_height
    regions.append((x, y, cell_width, cell_height, 0, 0))

# Create the scatter matrix with ggbunch
matrix = ggbunch(plots, regions)

# Add title, axis labels, and legend using a wrapper approach
# Create a title plot
title_plot = (
    ggplot()
    + geom_blank()
    + ggtitle("scatter-matrix-interactive · letsplot · pyplots.ai")
    + theme_void()
    + theme(plot_title=element_text(size=24, hjust=0.5))
)

# Create a legend plot with all three species
legend_df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 1, 1], "Species": ["Setosa", "Versicolor", "Virginica"]})
legend_plot = (
    ggplot(legend_df, aes(x="x", y="y", color="Species", fill="Species"))
    + geom_point(size=6, alpha=0.7, shape=21)
    + scale_color_manual(values=colors)
    + scale_fill_manual(values=colors)
    + theme_void()
    + theme(
        legend_position="bottom",
        legend_direction="horizontal",
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
    )
    + guides(color=guide_legend(nrow=1), fill=guide_legend(nrow=1))
)

# Combine all elements
final_plots = [title_plot] + plots + [legend_plot]
final_regions = [(0, 0, 1, title_height, 0, 0)]  # Title
final_regions.extend(regions)  # Matrix
final_regions.append((0.2, 1 - legend_height, 0.6, legend_height, 0, 0))  # Legend

final_plot = ggbunch(final_plots, final_regions) + ggsize(1200, 1200)

# Save outputs to current directory
ggsave(final_plot, "plot.png", path=".", scale=3)
ggsave(final_plot, "plot.html", path=".")
