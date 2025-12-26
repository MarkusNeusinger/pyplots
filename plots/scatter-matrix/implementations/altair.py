"""pyplots.ai
scatter-matrix: Scatter Plot Matrix
Library: altair 6.0.0 | Python 3.13.11
Quality: 65/100 | Created: 2025-12-26
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Iris dataset (classic multivariate data)
np.random.seed(42)

# Generate realistic iris-like data with 4 variables and 3 species
n_per_species = 50

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

# Color scheme - Distinct colorblind-safe palette (blue, orange, green)
color_scale = alt.Scale(domain=["Setosa", "Versicolor", "Virginica"], range=["#306998", "#E69F00", "#009E73"])

# Build the scatter matrix with histograms on diagonal
# Each cell is 350x350, with 4x4 grid = 1400x1400 base
cell_size = 350
charts = []

for i, row_var in enumerate(variables):
    row_charts = []
    for j, col_var in enumerate(variables):
        if i == j:
            # Diagonal: layered histograms showing distribution by species
            # Create separate histograms for each species and layer them
            hist_layers = []
            for species_name in ["Setosa", "Versicolor", "Virginica"]:
                species_df = df[df["Species"] == species_name]
                hist_layer = (
                    alt.Chart(species_df)
                    .mark_bar(opacity=0.6)
                    .encode(
                        alt.X(
                            f"{col_var}:Q",
                            bin=alt.Bin(maxbins=12),
                            title=col_var if i == len(variables) - 1 else "",
                            axis=alt.Axis(labelFontSize=16, titleFontSize=20),
                        ),
                        alt.Y(
                            "count():Q",
                            title="Count" if j == 0 else "",
                            axis=alt.Axis(labelFontSize=16, titleFontSize=20),
                        ),
                        color=alt.value(color_scale.range[["Setosa", "Versicolor", "Virginica"].index(species_name)]),
                        tooltip=[alt.Tooltip("count():Q", title="Count")],
                    )
                    .properties(width=cell_size, height=cell_size)
                )
                hist_layers.append(hist_layer)
            hist = alt.layer(*hist_layers)
            row_charts.append(hist)
        else:
            # Off-diagonal: scatter plot
            scatter = (
                alt.Chart(df)
                .mark_circle(size=80, opacity=0.7)
                .encode(
                    alt.X(
                        f"{col_var}:Q",
                        title=col_var if i == len(variables) - 1 else "",
                        axis=alt.Axis(labelFontSize=16, titleFontSize=20),
                    ),
                    alt.Y(
                        f"{row_var}:Q",
                        title=row_var if j == 0 else "",
                        axis=alt.Axis(labelFontSize=16, titleFontSize=20),
                    ),
                    alt.Color("Species:N", scale=color_scale, legend=None),
                    tooltip=["Species:N", f"{col_var}:Q", f"{row_var}:Q"],
                )
                .properties(width=cell_size, height=cell_size)
            )
            row_charts.append(scatter)
    charts.append(alt.hconcat(*row_charts, spacing=5))

# Create a legend chart to display alongside the matrix
legend_data = pd.DataFrame({"Species": ["Setosa", "Versicolor", "Virginica"]})
legend_chart = (
    alt.Chart(legend_data)
    .mark_point(size=400, filled=True)
    .encode(
        alt.Y("Species:N", axis=alt.Axis(orient="right", labelFontSize=26, titleFontSize=28, title=None)),
        alt.Color("Species:N", scale=color_scale, legend=None),
    )
    .properties(width=50, height=200, title=alt.Title(text="Species", fontSize=28, anchor="middle"))
)

# Combine all rows vertically
matrix = alt.vconcat(*charts, spacing=5).properties(
    title=alt.Title(text="scatter-matrix · altair · pyplots.ai", fontSize=36, anchor="middle", offset=20)
)

# Combine matrix with legend
combined = alt.hconcat(matrix, legend_chart, spacing=30)

# Apply configuration for consistent styling
chart = combined.configure_axis(gridOpacity=0.3).configure_view(strokeWidth=0)

# Save as PNG (scale_factor=3 gives us ~4200x4200 for 4 variables at 350px each)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
