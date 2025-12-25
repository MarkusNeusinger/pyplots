"""pyplots.ai
heatmap-correlation: Correlation Matrix Heatmap
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    labs,
    scale_fill_gradient2,
    theme,
    theme_minimal,
)


# Data - realistic financial/portfolio variables
np.random.seed(42)

variables = ["Stock_A", "Stock_B", "Stock_C", "Bonds", "Gold", "Real_Estate", "Oil", "Tech_Index"]

# Create a realistic correlation matrix with varied correlations
n_vars = len(variables)
base_corr = np.array(
    [
        [1.00, 0.85, 0.72, -0.35, -0.15, 0.42, 0.28, 0.91],  # Stock_A
        [0.85, 1.00, 0.68, -0.28, -0.22, 0.38, 0.31, 0.82],  # Stock_B
        [0.72, 0.68, 1.00, -0.18, -0.08, 0.52, 0.45, 0.75],  # Stock_C
        [-0.35, -0.28, -0.18, 1.00, 0.45, 0.12, -0.25, -0.32],  # Bonds
        [-0.15, -0.22, -0.08, 0.45, 1.00, 0.08, 0.35, -0.18],  # Gold
        [0.42, 0.38, 0.52, 0.12, 0.08, 1.00, 0.22, 0.48],  # Real_Estate
        [0.28, 0.31, 0.45, -0.25, 0.35, 0.22, 1.00, 0.32],  # Oil
        [0.91, 0.82, 0.75, -0.32, -0.18, 0.48, 0.32, 1.00],  # Tech_Index
    ]
)

# Convert matrix to long format for plotnine
rows = []
for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        rows.append({"Var1": var1, "Var2": var2, "Correlation": base_corr[i, j]})

df = pd.DataFrame(rows)

# Set categorical order to maintain variable arrangement
df["Var1"] = pd.Categorical(df["Var1"], categories=variables, ordered=True)
df["Var2"] = pd.Categorical(df["Var2"], categories=variables[::-1], ordered=True)

# Create heatmap
plot = (
    ggplot(df, aes(x="Var1", y="Var2", fill="Correlation"))
    + geom_tile(color="white", size=0.5)
    + geom_text(aes(label="Correlation"), format_string="{:.2f}", size=12, color="black")
    + scale_fill_gradient2(
        low="#2166AC",  # Blue for negative
        mid="white",  # White for zero
        high="#B2182B",  # Red for positive
        midpoint=0,
        limits=(-1, 1),
        name="Correlation",
    )
    + coord_fixed(ratio=1)
    + labs(title="heatmap-correlation · plotnine · pyplots.ai", x="Variable", y="Variable")
    + theme_minimal()
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=24, ha="center", weight="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=14, rotation=45, ha="right"),
        axis_text_y=element_text(size=14),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, width=12, height=12)
