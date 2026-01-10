"""pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-10
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_blank,
    geom_histogram,
    geom_point,
    geom_text,
    ggbunch,
    ggplot,
    ggsave,
    ggsize,
    ggtitle,
    guide_legend,
    guides,
    layer_tooltips,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
    theme_void,
)


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

# Color palette - accessible colors with good contrast on white background
# Using blue, orange (instead of yellow for better contrast), and teal
colors = ["#306998", "#E67E22", "#16A085"]

# Shortened variable labels for matrix edges (full names in tooltips)
short_labels = ["Sepal L", "Sepal W", "Petal L", "Petal W"]

# Create individual plots for the 4x4 matrix
plots = []
for i, var_y in enumerate(variables):
    for j, var_x in enumerate(variables):
        # Determine if we need axis labels
        show_x_label = i == n - 1  # Bottom row shows x labels
        show_y_label = j == 0  # Left column shows y labels

        if i == j:
            # Diagonal: histogram showing distribution
            p = (
                ggplot(df, aes(x=var_x, fill="Species"))
                + geom_histogram(alpha=0.7, bins=15, position="identity")
                + scale_fill_manual(values=colors)
                + theme_minimal()
                + theme(
                    axis_title_x=element_text(size=12) if show_x_label else element_blank(),
                    axis_title_y=element_blank(),
                    axis_text=element_text(size=10),
                    legend_position="none",
                    plot_margin=[5, 5, 5, 5],
                )
            )
            # Add variable name in diagonal cell
            if show_x_label:
                p = p + ggtitle(short_labels[j])
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
                    .line(f"{var_x}: @{{{var_x}}}")
                    .line(f"{var_y}: @{{{var_y}}}"),
                )
                + scale_color_manual(values=colors)
                + scale_fill_manual(values=colors)
                + theme_minimal()
                + theme(
                    axis_title_x=element_text(size=12) if show_x_label else element_blank(),
                    axis_title_y=element_text(size=12) if show_y_label else element_blank(),
                    axis_text=element_text(size=10),
                    legend_position="none",
                    plot_margin=[5, 5, 5, 5],
                )
            )
        plots.append(p)

# Calculate regions for ggbunch (4x4 grid)
# Leave space for title at top, labels on left/bottom, and legend at bottom
title_height = 0.07
legend_height = 0.06
label_width = 0.08  # Space for row labels on left
label_height = 0.06  # Space for column labels at bottom
grid_width = 1.0 - label_width
grid_height = 1.0 - title_height - legend_height - label_height
cell_width = grid_width / n
cell_height = grid_height / n

regions = []
for idx in range(n * n):
    row = idx // n
    col = idx % n
    x = label_width + col * cell_width
    y = title_height + row * cell_height
    regions.append((x, y, cell_width, cell_height, 0, 0))

# Create the scatter matrix with ggbunch
matrix = ggbunch(plots, regions)

# Add title
title_plot = (
    ggplot()
    + geom_blank()
    + ggtitle("scatter-matrix-interactive · letsplot · pyplots.ai")
    + theme_void()
    + theme(plot_title=element_text(size=24, hjust=0.5))
)

# Create column label plots (at bottom)
col_label_plots = []
for label in short_labels:
    label_df = pd.DataFrame({"x": [0], "y": [0], "label": [label]})
    col_label_plot = ggplot(label_df, aes(x="x", y="y", label="label")) + geom_text(size=14) + theme_void()
    col_label_plots.append(col_label_plot)

# Create row label plots (on left side)
row_label_plots = []
for label in short_labels:
    label_df = pd.DataFrame({"x": [0], "y": [0], "label": [label]})
    row_label_plot = ggplot(label_df, aes(x="x", y="y", label="label")) + geom_text(size=14, angle=90) + theme_void()
    row_label_plots.append(row_label_plot)

# Create a legend plot with all three species - only showing the legend
legend_df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 1, 1], "Species": ["Setosa", "Versicolor", "Virginica"]})
legend_plot = (
    ggplot(legend_df, aes(x="x", y="y", color="Species", fill="Species"))
    + geom_point(size=8, alpha=0.0, shape=21)  # Invisible points, only for legend
    + scale_color_manual(values=colors)
    + scale_fill_manual(values=colors)
    + theme_void()
    + theme(
        legend_position="bottom",
        legend_direction="horizontal",
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
    )
    + guides(color=guide_legend(nrow=1, override_aes={"alpha": 0.7}), fill=guide_legend(nrow=1))
)

# Combine all elements
final_plots = [title_plot]  # Title
final_plots.extend(plots)  # Matrix plots
final_plots.extend(col_label_plots)  # Column labels
final_plots.extend(row_label_plots)  # Row labels
final_plots.append(legend_plot)  # Legend

# Define regions
final_regions = [(0, 0, 1, title_height, 0, 0)]  # Title

# Matrix regions
for idx in range(n * n):
    row = idx // n
    col = idx % n
    x = label_width + col * cell_width
    y = title_height + row * cell_height
    final_regions.append((x, y, cell_width, cell_height, 0, 0))

# Column label regions (below matrix)
col_label_y = title_height + grid_height
for j in range(n):
    x = label_width + j * cell_width
    final_regions.append((x, col_label_y, cell_width, label_height, 0, 0))

# Row label regions (left of matrix)
for i in range(n):
    y = title_height + i * cell_height
    final_regions.append((0, y, label_width, cell_height, 0, 0))

# Legend region (at bottom)
final_regions.append((0.15, 1 - legend_height, 0.7, legend_height, 0, 0))

final_plot = ggbunch(final_plots, final_regions) + ggsize(1200, 1200)

# Save outputs to current directory
ggsave(final_plot, "plot.png", path=".", scale=3)
ggsave(final_plot, "plot.html", path=".")
