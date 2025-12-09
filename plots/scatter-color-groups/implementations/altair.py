"""
scatter-color-groups: Scatter Plot with Color Groups
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - create iris-like dataset with three species groups
np.random.seed(42)

# Generate data for three groups with different cluster centers
n_per_group = 50

# Setosa: smaller sepal length, larger sepal width
setosa_x = np.random.normal(5.0, 0.4, n_per_group)
setosa_y = np.random.normal(3.4, 0.4, n_per_group)

# Versicolor: medium values
versicolor_x = np.random.normal(6.0, 0.5, n_per_group)
versicolor_y = np.random.normal(2.8, 0.3, n_per_group)

# Virginica: larger sepal length, medium sepal width
virginica_x = np.random.normal(6.6, 0.6, n_per_group)
virginica_y = np.random.normal(3.0, 0.35, n_per_group)

data = pd.DataFrame(
    {
        "sepal_length": np.concatenate([setosa_x, versicolor_x, virginica_x]),
        "sepal_width": np.concatenate([setosa_y, versicolor_y, virginica_y]),
        "species": ["setosa"] * n_per_group + ["versicolor"] * n_per_group + ["virginica"] * n_per_group,
    }
)

# Define custom color palette (colorblind-safe)
color_scale = alt.Scale(domain=["setosa", "versicolor", "virginica"], range=["#306998", "#FFD43B", "#059669"])

# Create scatter plot with color groups
chart = (
    alt.Chart(data)
    .mark_point(size=100, opacity=0.7)
    .encode(
        x=alt.X("sepal_length:Q", title="Sepal Length (cm)"),
        y=alt.Y("sepal_width:Q", title="Sepal Width (cm)"),
        color=alt.Color("species:N", title="Species", scale=color_scale),
        tooltip=["species:N", "sepal_length:Q", "sepal_width:Q"],
    )
    .properties(width=1600, height=900, title="Scatter Plot with Color Groups")
)

# Save as PNG (1600 × 900 × 3 = 4800 × 2700 px)
chart.save("plot.png", scale_factor=3.0)
