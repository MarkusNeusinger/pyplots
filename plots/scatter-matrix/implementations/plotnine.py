""" pyplots.ai
scatter-matrix: Scatter Plot Matrix
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 83/100 | Created: 2025-12-26
"""

import warnings

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_text,
    facet_grid,
    geom_density,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
)


warnings.filterwarnings("ignore")

# Data - Iris-like data for multivariate visualization
np.random.seed(42)

species = np.repeat(["setosa", "versicolor", "virginica"], 50)

# Generate correlated data for each species with realistic iris measurements
data = {
    "Sepal Length": np.concatenate(
        [np.random.normal(5.0, 0.35, 50), np.random.normal(5.9, 0.5, 50), np.random.normal(6.6, 0.6, 50)]
    ),
    "Sepal Width": np.concatenate(
        [np.random.normal(3.4, 0.4, 50), np.random.normal(2.8, 0.3, 50), np.random.normal(3.0, 0.3, 50)]
    ),
    "Petal Length": np.concatenate(
        [np.random.normal(1.5, 0.2, 50), np.random.normal(4.3, 0.5, 50), np.random.normal(5.5, 0.5, 50)]
    ),
    "Petal Width": np.concatenate(
        [np.random.normal(0.25, 0.1, 50), np.random.normal(1.3, 0.2, 50), np.random.normal(2.0, 0.3, 50)]
    ),
    "Species": species,
}

df = pd.DataFrame(data)

# Variables for the matrix
variables = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]

# Create long-form data for faceted scatter matrix
# Only off-diagonal cells for scatter, diagonal cells for density
scatter_rows = []
diag_rows = []

for var_y in variables:
    for var_x in variables:
        is_diag = var_x == var_y
        for idx in range(len(df)):
            row = {
                "x": df[var_x].iloc[idx],
                "y": df[var_y].iloc[idx],
                "var_x": var_x,
                "var_y": var_y,
                "Species": df["Species"].iloc[idx],
            }
            if is_diag:
                diag_rows.append(row)
            else:
                scatter_rows.append(row)

scatter_df = pd.DataFrame(scatter_rows)
diag_df = pd.DataFrame(diag_rows)

# Colors - Python Blue, Python Yellow, and complementary coral
colors = ["#306998", "#FFD43B", "#E07A5F"]

# Create scatter matrix using facet_grid
# Scatter plots on off-diagonal, density curves on diagonal
plot = (
    ggplot(scatter_df, aes(x="x", y="y", color="Species"))
    # Scatter for off-diagonal cells
    + geom_point(size=2.5, alpha=0.7)
    # KDE for diagonal cells
    + geom_density(aes(x="x", fill="Species", color="Species"), data=diag_df, alpha=0.4)
    + facet_grid("var_y ~ var_x", scales="free")
    + scale_color_manual(values=colors)
    + scale_fill_manual(values=colors)
    + labs(title="Iris Dataset · scatter-matrix · plotnine · pyplots.ai", x="", y="")
    + theme_minimal()
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=18, face="bold", ha="center"),
        strip_text=element_text(size=11, face="bold"),
        axis_text=element_text(size=9),
        legend_title=element_text(size=12),
        legend_text=element_text(size=11),
        legend_position="right",
        panel_spacing=0.03,
    )
)

# Save the plot
plot.save("plot.png", dpi=300, width=12, height=12, verbose=False)
