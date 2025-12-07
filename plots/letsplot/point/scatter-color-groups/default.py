"""
scatter-color-groups: Scatter Plot with Color Groups
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Generate iris-like dataset
np.random.seed(42)
n_per_species = 50

# Setosa: smaller sepals
setosa_length = np.random.normal(5.0, 0.35, n_per_species)
setosa_width = np.random.normal(3.4, 0.38, n_per_species)

# Versicolor: medium sepals
versicolor_length = np.random.normal(5.9, 0.52, n_per_species)
versicolor_width = np.random.normal(2.8, 0.31, n_per_species)

# Virginica: larger sepals
virginica_length = np.random.normal(6.6, 0.64, n_per_species)
virginica_width = np.random.normal(3.0, 0.32, n_per_species)

data = pd.DataFrame(
    {
        "sepal_length": np.concatenate([setosa_length, versicolor_length, virginica_length]),
        "sepal_width": np.concatenate([setosa_width, versicolor_width, virginica_width]),
        "species": ["Setosa"] * n_per_species + ["Versicolor"] * n_per_species + ["Virginica"] * n_per_species,
    }
)

# Custom color palette (colorblind-safe)
colors = ["#306998", "#FFD43B", "#059669"]

# Plot
plot = (
    ggplot(data, aes(x="sepal_length", y="sepal_width", color="species"))
    + geom_point(size=4, alpha=0.7)
    + scale_color_manual(values=colors)
    + labs(x="Sepal Length (cm)", y="Sepal Width (cm)", title="Iris Sepal Dimensions by Species", color="Species")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=20),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=16),
        legend_text=element_text(size=16),
    )
    + ggsize(1600, 900)
)

# Save (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)
