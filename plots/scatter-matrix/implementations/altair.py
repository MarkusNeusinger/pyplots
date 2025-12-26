""" pyplots.ai
scatter-matrix: Scatter Plot Matrix
Library: altair 6.0.0 | Python 3.13.11
Quality: 80/100 | Created: 2025-12-26
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Iris dataset (classic multivariate data)
np.random.seed(42)

# Generate realistic iris-like data with 4 variables and 3 species
n_per_species = 50
species = ["Setosa", "Versicolor", "Virginica"]

data = []
# Setosa - smaller flowers
for _ in range(n_per_species):
    data.append(
        {
            "Sepal Length (cm)": np.random.normal(5.0, 0.35),
            "Sepal Width (cm)": np.random.normal(3.4, 0.38),
            "Petal Length (cm)": np.random.normal(1.5, 0.17),
            "Petal Width (cm)": np.random.normal(0.25, 0.1),
            "Species": "Setosa",
        }
    )

# Versicolor - medium flowers
for _ in range(n_per_species):
    data.append(
        {
            "Sepal Length (cm)": np.random.normal(5.9, 0.52),
            "Sepal Width (cm)": np.random.normal(2.8, 0.31),
            "Petal Length (cm)": np.random.normal(4.3, 0.47),
            "Petal Width (cm)": np.random.normal(1.3, 0.2),
            "Species": "Versicolor",
        }
    )

# Virginica - larger flowers
for _ in range(n_per_species):
    data.append(
        {
            "Sepal Length (cm)": np.random.normal(6.6, 0.64),
            "Sepal Width (cm)": np.random.normal(3.0, 0.32),
            "Petal Length (cm)": np.random.normal(5.5, 0.55),
            "Petal Width (cm)": np.random.normal(2.0, 0.27),
            "Species": "Virginica",
        }
    )

df = pd.DataFrame(data)

# Variables for the scatter matrix
variables = ["Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"]

# Color scheme - Python Blue based palette that's colorblind-safe
color_scale = alt.Scale(domain=["Setosa", "Versicolor", "Virginica"], range=["#306998", "#FFD43B", "#4B8BBE"])

# Create scatter matrix using repeat
scatter = (
    alt.Chart(df)
    .mark_circle(size=80, opacity=0.7)
    .encode(
        alt.X(alt.repeat("column"), type="quantitative"),
        alt.Y(alt.repeat("row"), type="quantitative"),
        color=alt.Color(
            "Species:N",
            scale=color_scale,
            legend=alt.Legend(titleFontSize=20, labelFontSize=18, symbolSize=200, orient="right"),
        ),
        tooltip=["Species:N"] + [f"{v}:Q" for v in variables],
    )
    .properties(width=350, height=350)
)

# Create the matrix by repeating across rows and columns
chart = (
    scatter.repeat(row=variables, column=variables)
    .properties(
        title=alt.Title(
            text="Iris Dataset · scatter-matrix · altair · pyplots.ai", fontSize=32, anchor="middle", offset=20
        )
    )
    .configure_axis(labelFontSize=14, titleFontSize=18, gridOpacity=0.3)
    .configure_view(strokeWidth=1, stroke="#ccc")
    .configure_title(fontSize=32)
)

# Save as PNG (scale_factor=3 gives us ~4200x4200 for 4 variables at 350px each)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
