""" pyplots.ai
scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)
Library: plotly 6.5.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-10
"""

import numpy as np
import plotly.express as px
import seaborn as sns


# Data - Using Iris dataset for multivariate exploration
np.random.seed(42)
iris = sns.load_dataset("iris")
iris = iris.rename(
    columns={
        "sepal_length": "Sepal Length (cm)",
        "sepal_width": "Sepal Width (cm)",
        "petal_length": "Petal Length (cm)",
        "petal_width": "Petal Width (cm)",
        "species": "Species",
    }
)

# Capitalize species names for display
iris["Species"] = iris["Species"].str.capitalize()

# Color mapping for species (Python branding colors + complementary)
color_discrete_map = {
    "Setosa": "#306998",  # Python Blue
    "Versicolor": "#FFD43B",  # Python Yellow
    "Virginica": "#4ECDC4",  # Teal for third category
}

# Create scatter matrix (SPLOM) with linked brushing using plotly express
fig = px.scatter_matrix(
    iris,
    dimensions=["Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"],
    color="Species",
    color_discrete_map=color_discrete_map,
    title="Iris Dataset · scatter-matrix-interactive · plotly · pyplots.ai",
    opacity=0.7,
)

# Update marker styling for better visibility
fig.update_traces(
    marker=dict(size=8, line=dict(width=0.5, color="white")),
    diagonal_visible=True,
    showupperhalf=True,
    # Enable linked selection across all subplots
    selected=dict(marker=dict(opacity=1.0, size=10)),
    unselected=dict(marker=dict(opacity=0.15, size=6)),
)

# Layout for large canvas with interactivity
fig.update_layout(
    title=dict(
        text="Iris Dataset · scatter-matrix-interactive · plotly · pyplots.ai",
        font=dict(size=28),
        x=0.5,
        xanchor="center",
    ),
    font=dict(size=16),
    # Enable dragmode for box selection
    dragmode="select",
    # Subplot configuration
    width=1600,
    height=1500,
    template="plotly_white",
    # Legend configuration
    legend=dict(
        title=dict(text="Species", font=dict(size=18)),
        font=dict(size=16),
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#CCCCCC",
        borderwidth=1,
    ),
    # Margins for labels and legend
    margin=dict(l=80, r=150, t=100, b=80),
)

# Save as PNG (3600x3600 for square format)
fig.write_image("plot.png", width=1200, height=1200, scale=3)

# Save interactive HTML version with full interactivity
fig.write_html(
    "plot.html",
    include_plotlyjs=True,
    full_html=True,
    config={"displayModeBar": True, "modeBarButtonsToAdd": ["select2d", "lasso2d"], "scrollZoom": True},
)
