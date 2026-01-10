""" pyplots.ai
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
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
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

# Colors for species - Python Blue as primary, with complementary colors
colors = ["#306998", "#FFD43B", "#E74C3C"]

# Create long-form data for scatter plots (off-diagonal only)
scatter_data = []
for var_y in variables:
    for var_x in variables:
        if var_x != var_y:  # Only off-diagonal
            temp_df = df[[var_x, var_y, "Species"]].copy()
            temp_df.columns = ["x", "y", "Species"]
            temp_df["var_x"] = var_x
            temp_df["var_y"] = var_y
            scatter_data.append(temp_df)

scatter_df = pd.concat(scatter_data, ignore_index=True)

# Set factor levels for proper ordering
scatter_df["var_x"] = pd.Categorical(scatter_df["var_x"], categories=variables)
scatter_df["var_y"] = pd.Categorical(scatter_df["var_y"], categories=variables[::-1])

# Create scatter plot matrix
plot = (
    ggplot(scatter_df, aes(x="x", y="y", color="Species"))
    + geom_point(size=3, alpha=0.7)
    + facet_grid("var_y ~ var_x", scales="free")
    + scale_color_manual(values=colors)
    + labs(
        title="scatter-matrix-interactive · plotnine · pyplots.ai",
        subtitle="Iris Dataset Pairwise Relationships (Static - Interactive brushing requires Plotly/Bokeh/Altair)",
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
        legend_background=element_rect(fill="white", alpha=0.8),
        panel_spacing=0.03,
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="#f8f8f8"),
    )
)

# Save plot
plot.save("plot.png", dpi=300, width=16, height=16, verbose=False)
