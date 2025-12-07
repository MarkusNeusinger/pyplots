"""
scatter-color-groups: Scatter Plot with Color Groups
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, geom_point, ggplot, labs, scale_color_manual, theme, theme_minimal


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
colors = ["#306998", "#FFD43B", "#DC2626"]

# Create plot
plot = (
    ggplot(data, aes(x="sepal_length", y="sepal_width", color="species"))
    + geom_point(size=3, alpha=0.7)
    + labs(x="Sepal Length (cm)", y="Sepal Width (cm)", title="Scatter Plot with Color Groups", color="Species")
    + scale_color_manual(values=colors)
    + theme_minimal()
    + theme(figure_size=(16, 9))
)

# Save
plot.save("plot.png", dpi=300)
