"""pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-10
"""

import warnings

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_rect,
    element_text,
    facet_grid,
    geom_histogram,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
)
from sklearn.datasets import load_iris


warnings.filterwarnings("ignore")

# Data: Iris dataset for multivariate analysis
np.random.seed(42)
iris = load_iris()
df = pd.DataFrame(iris.data, columns=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"])
df["Species"] = pd.Categorical([iris.target_names[i] for i in iris.target])

# Select 4 variables for the matrix
variables = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
# Units for each variable
units = {"Sepal Length": "cm", "Sepal Width": "cm", "Petal Length": "cm", "Petal Width": "cm"}

# Colorblind-safe palette (Dark2 inspired - teal, orange, purple)
colors = ["#1B9E77", "#D95F02", "#7570B3"]

# Create long-form data for scatter plots (off-diagonal only)
scatter_data = []
for var_y in variables:
    for var_x in variables:
        if var_x != var_y:  # Only off-diagonal
            temp_df = df[[var_x, var_y, "Species"]].copy()
            temp_df.columns = ["x", "y", "Species"]
            temp_df["var_x"] = f"{var_x} ({units[var_x]})"
            temp_df["var_y"] = f"{var_y} ({units[var_y]})"
            scatter_data.append(temp_df)

scatter_df = pd.concat(scatter_data, ignore_index=True)

# Create long-form data for histograms (diagonal only)
hist_data = []
for var in variables:
    temp_df = df[[var, "Species"]].copy()
    temp_df.columns = ["x", "Species"]
    temp_df["var_x"] = f"{var} ({units[var]})"
    temp_df["var_y"] = f"{var} ({units[var]})"
    hist_data.append(temp_df)

hist_df = pd.concat(hist_data, ignore_index=True)

# Set factor levels for proper ordering with units
var_labels = [f"{v} ({units[v]})" for v in variables]
scatter_df["var_x"] = pd.Categorical(scatter_df["var_x"], categories=var_labels)
scatter_df["var_y"] = pd.Categorical(scatter_df["var_y"], categories=var_labels[::-1])
hist_df["var_x"] = pd.Categorical(hist_df["var_x"], categories=var_labels)
hist_df["var_y"] = pd.Categorical(hist_df["var_y"], categories=var_labels[::-1])

# Create scatter plot matrix with diagonal histograms using layer composition
# The key is that geom_histogram has its own aes() that doesn't include y
plot = (
    ggplot(mapping=aes(x="x"))
    + geom_point(data=scatter_df, mapping=aes(y="y", color="Species"), size=4, alpha=0.7)
    + geom_histogram(data=hist_df, mapping=aes(fill="Species"), bins=12, alpha=0.7, position="identity")
    + facet_grid("var_y ~ var_x", scales="free")
    + scale_color_manual(values=colors)
    + scale_fill_manual(values=colors)
    + labs(
        title="scatter-matrix-interactive · plotnine · pyplots.ai",
        subtitle="Iris Dataset: Pairwise Scatter Plots with Univariate Distributions (Static)",
        x="",
        y="",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 16),
        plot_title=element_text(size=24, weight="bold", ha="left"),
        plot_subtitle=element_text(size=14, color="#666666"),
        strip_text_x=element_text(size=13),
        strip_text_y=element_text(size=13, angle=0),
        axis_text=element_text(size=11),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="bottom",
        legend_background=element_rect(fill="white", alpha=0.9),
        panel_spacing=0.03,
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="#f8f8f8"),
    )
)

# Save plot
plot.save("plot.png", dpi=300, width=16, height=16, verbose=False)
