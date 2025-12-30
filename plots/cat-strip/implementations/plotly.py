"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Fruit yields across different orchard sections
np.random.seed(42)

categories = ["Section A", "Section B", "Section C", "Section D"]
n_per_category = 25

# Different distributions per category to show variation
data = {
    "Section A": np.random.normal(45, 8, n_per_category),  # High yield
    "Section B": np.random.normal(32, 12, n_per_category),  # Medium, spread
    "Section C": np.random.normal(28, 5, n_per_category),  # Lower, tight
    "Section D": np.random.normal(38, 10, n_per_category),  # Medium-high
}

# Create figure
fig = go.Figure()

# Add strip plot for each category with jitter
for i, (category, values) in enumerate(data.items()):
    # Add jitter to x-position
    jitter = np.random.uniform(-0.25, 0.25, len(values))
    x_positions = np.full(len(values), i) + jitter

    fig.add_trace(
        go.Scatter(
            x=x_positions,
            y=values,
            mode="markers",
            name=category,
            marker={
                "size": 14,
                "opacity": 0.7,
                "color": "#306998" if i % 2 == 0 else "#FFD43B",
                "line": {"width": 1, "color": "#1a3d5c" if i % 2 == 0 else "#c9a82c"},
            },
            hovertemplate=f"{category}<br>Yield: %{{y:.1f}} kg<extra></extra>",
        )
    )

# Layout
fig.update_layout(
    title={"text": "cat-strip · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Orchard Section", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "tickmode": "array",
        "tickvals": [0, 1, 2, 3],
        "ticktext": categories,
        "showgrid": False,
    },
    yaxis={
        "title": {"text": "Fruit Yield (kg)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    showlegend=False,
    plot_bgcolor="white",
    margin={"l": 100, "r": 80, "t": 120, "b": 100},
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
