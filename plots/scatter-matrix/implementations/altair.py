"""pyplots.ai
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

# Build the scatter matrix with histograms on diagonal manually
# Each cell is 350x350, with 4x4 grid = 1400x1400 base
cell_size = 350
charts = []

for i, row_var in enumerate(variables):
    row_charts = []
    for j, col_var in enumerate(variables):
        if i == j:
            # Diagonal: histogram showing distribution by species
            hist = (
                alt.Chart(df)
                .mark_bar(opacity=0.7)
                .encode(
                    alt.X(f"{col_var}:Q", bin=alt.Bin(maxbins=15), title=col_var if i == len(variables) - 1 else ""),
                    alt.Y("count():Q", stack=None, title=row_var if j == 0 else ""),
                    alt.Color(
                        "Species:N",
                        scale=color_scale,
                        legend=alt.Legend(
                            titleFontSize=24, labelFontSize=22, symbolSize=300, orient="right", title="Species"
                        )
                        if i == 0 and j == 0
                        else None,
                    ),
                    tooltip=["Species:N", alt.Tooltip("count():Q", title="Count")],
                )
                .properties(width=cell_size, height=cell_size)
            )
            row_charts.append(hist)
        else:
            # Off-diagonal: scatter plot
            scatter = (
                alt.Chart(df)
                .mark_circle(size=80, opacity=0.7)
                .encode(
                    alt.X(f"{col_var}:Q", title=col_var if i == len(variables) - 1 else ""),
                    alt.Y(f"{row_var}:Q", title=row_var if j == 0 else ""),
                    alt.Color("Species:N", scale=color_scale, legend=None),
                    tooltip=["Species:N", f"{col_var}:Q", f"{row_var}:Q"],
                )
                .properties(width=cell_size, height=cell_size)
            )
            row_charts.append(scatter)
    charts.append(alt.hconcat(*row_charts, spacing=5))

# Combine all rows vertically
matrix = alt.vconcat(*charts, spacing=5).properties(
    title=alt.Title(text="Iris Dataset · scatter-matrix · altair · pyplots.ai", fontSize=32, anchor="middle", offset=20)
)

# Apply configuration for consistent styling
chart = matrix.configure_axis(labelFontSize=14, titleFontSize=18, gridOpacity=0.3).configure_view(
    strokeWidth=1, stroke="#ccc"
)

# Save as PNG (scale_factor=3 gives us ~4200x4200 for 4 variables at 350px each)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
