""" pyplots.ai
parallel-basic: Basic Parallel Coordinates Plot
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)


# Data - Iris dataset
np.random.seed(42)
iris_data = {
    "sepal_length": [
        5.1,
        4.9,
        4.7,
        4.6,
        5.0,
        5.4,
        4.6,
        5.0,
        4.4,
        4.9,
        7.0,
        6.4,
        6.9,
        5.5,
        6.5,
        5.7,
        6.3,
        4.9,
        6.6,
        5.2,
        6.3,
        5.8,
        7.1,
        6.3,
        6.5,
        7.6,
        4.9,
        7.3,
        6.7,
        7.2,
        5.9,
        6.0,
        5.5,
        6.2,
        5.4,
        6.7,
        6.3,
        5.6,
        5.5,
        5.8,
        6.0,
        5.4,
        6.0,
        6.7,
        6.3,
        5.6,
        5.5,
        5.5,
        6.1,
        5.8,
    ],
    "sepal_width": [
        3.5,
        3.0,
        3.2,
        3.1,
        3.6,
        3.9,
        3.4,
        3.4,
        2.9,
        3.1,
        3.2,
        3.2,
        3.1,
        2.3,
        2.8,
        2.8,
        3.3,
        2.4,
        2.9,
        2.7,
        3.3,
        2.7,
        3.0,
        2.9,
        3.0,
        3.0,
        2.5,
        2.9,
        2.5,
        3.6,
        3.2,
        2.7,
        2.6,
        2.9,
        3.0,
        3.1,
        2.3,
        3.0,
        2.5,
        2.8,
        2.2,
        3.0,
        2.2,
        3.0,
        2.5,
        2.8,
        2.6,
        2.4,
        3.0,
        2.7,
    ],
    "petal_length": [
        1.4,
        1.4,
        1.3,
        1.5,
        1.4,
        1.7,
        1.4,
        1.5,
        1.4,
        1.5,
        4.7,
        4.5,
        4.9,
        4.0,
        4.6,
        4.5,
        4.7,
        3.3,
        4.6,
        3.9,
        6.0,
        5.1,
        5.9,
        5.6,
        5.8,
        6.6,
        4.5,
        6.3,
        5.8,
        6.1,
        4.8,
        5.1,
        4.0,
        4.3,
        4.5,
        5.6,
        4.4,
        4.1,
        4.0,
        4.4,
        5.0,
        4.5,
        5.0,
        5.2,
        4.9,
        4.9,
        4.4,
        3.8,
        4.9,
        5.1,
    ],
    "petal_width": [
        0.2,
        0.2,
        0.2,
        0.2,
        0.2,
        0.4,
        0.3,
        0.2,
        0.2,
        0.1,
        1.4,
        1.5,
        1.5,
        1.3,
        1.5,
        1.3,
        1.6,
        1.0,
        1.3,
        1.4,
        2.5,
        1.9,
        2.1,
        1.8,
        2.2,
        2.1,
        1.7,
        1.8,
        1.8,
        2.5,
        1.8,
        1.6,
        1.3,
        1.3,
        1.5,
        2.4,
        1.3,
        1.3,
        1.3,
        1.2,
        1.5,
        1.5,
        1.5,
        2.3,
        1.8,
        2.0,
        1.2,
        1.1,
        1.8,
        1.8,
    ],
    "species": ["setosa"] * 10 + ["versicolor"] * 10 + ["virginica"] * 10 + ["versicolor"] * 10 + ["virginica"] * 10,
}
df = pd.DataFrame(iris_data)
df["id"] = range(len(df))

# Normalize each dimension to 0-1 scale
dimensions = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
df_normalized = df.copy()
for col in dimensions:
    df_normalized[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Transform to long format for parallel coordinates
df_long = pd.melt(
    df_normalized, id_vars=["id", "species"], value_vars=dimensions, var_name="dimension", value_name="value"
)

# Map dimension names to numeric positions for x-axis
dim_map = {dim: i for i, dim in enumerate(dimensions)}
df_long["dim_num"] = df_long["dimension"].map(dim_map)

# Color palette - Python Blue for setosa, Yellow for versicolor, complementary for virginica
colors = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#E74C3C"}

# Create plot
plot = (
    ggplot(df_long, aes(x="dim_num", y="value", group="id", color="species"))
    + geom_line(alpha=0.6, size=1.2)
    + geom_point(size=3, alpha=0.7)
    + scale_color_manual(values=colors)
    + scale_x_continuous(
        breaks=list(range(len(dimensions))), labels=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
    )
    + labs(x="Dimension", y="Normalized Value", title="parallel-basic · plotnine · pyplots.ai", color="Species")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
