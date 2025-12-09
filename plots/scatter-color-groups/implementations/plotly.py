"""
scatter-color-groups: Scatter Plot with Color Groups
Library: plotly
"""

import numpy as np
import pandas as pd
import plotly.express as px


# Data - iris-like dataset with three species groups
np.random.seed(42)
n_per_group = 50

# Generate data for three species groups with distinct cluster patterns
setosa = pd.DataFrame(
    {
        "sepal_length": np.random.normal(5.0, 0.35, n_per_group),
        "sepal_width": np.random.normal(3.4, 0.38, n_per_group),
        "species": "setosa",
    }
)
versicolor = pd.DataFrame(
    {
        "sepal_length": np.random.normal(5.9, 0.52, n_per_group),
        "sepal_width": np.random.normal(2.8, 0.31, n_per_group),
        "species": "versicolor",
    }
)
virginica = pd.DataFrame(
    {
        "sepal_length": np.random.normal(6.6, 0.64, n_per_group),
        "sepal_width": np.random.normal(3.0, 0.32, n_per_group),
        "species": "virginica",
    }
)
data = pd.concat([setosa, versicolor, virginica], ignore_index=True)

# Color palette matching style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create plot
fig = px.scatter(
    data,
    x="sepal_length",
    y="sepal_width",
    color="species",
    color_discrete_sequence=colors,
    title="Scatter Plot with Color Groups",
)

# Update layout for styling
fig.update_layout(
    template="plotly_white",
    xaxis_title="Sepal Length (cm)",
    yaxis_title="Sepal Width (cm)",
    title={"font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    font={"size": 32},
    legend={"title": {"text": "Species", "font": {"size": 32}}, "font": {"size": 28}, "itemsizing": "constant"},
)

# Update axes for readability
fig.update_xaxes(title_font={"size": 40}, tickfont={"size": 32}, gridcolor="#E5E5E5")
fig.update_yaxes(title_font={"size": 40}, tickfont={"size": 32}, gridcolor="#E5E5E5")

# Update markers for better visibility
fig.update_traces(marker={"size": 16, "opacity": 0.8, "line": {"width": 1, "color": "white"}})

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)
