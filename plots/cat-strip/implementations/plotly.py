""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Plant growth measurements across different soil types
np.random.seed(42)
categories = ["Clay", "Sandy", "Loam", "Peat", "Chalk"]
n_per_category = 25

# Generate data with different distributions per category
data = {
    "Clay": np.random.normal(45, 8, n_per_category),
    "Sandy": np.random.normal(35, 12, n_per_category),
    "Loam": np.random.normal(60, 6, n_per_category),
    "Peat": np.random.normal(55, 10, n_per_category),
    "Chalk": np.random.normal(40, 15, n_per_category),
}

# Add some outliers
data["Sandy"] = np.append(data["Sandy"], [70, 72])
data["Loam"] = np.append(data["Loam"], [30])

# Create figure
fig = go.Figure()

# Add strip plot for each category with jitter
for i, (cat, values) in enumerate(data.items()):
    jitter = np.random.uniform(-0.2, 0.2, len(values))
    fig.add_trace(
        go.Scatter(
            x=np.full(len(values), i) + jitter,
            y=values,
            mode="markers",
            name=cat,
            marker=dict(size=14, opacity=0.7, line=dict(width=1, color="white")),
            hovertemplate=f"{cat}<br>Height: %{{y:.1f}} cm<extra></extra>",
        )
    )

# Layout
fig.update_layout(
    title=dict(text="cat-strip · plotly · pyplots.ai", font=dict(size=28), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="Soil Type", font=dict(size=22)),
        tickmode="array",
        tickvals=list(range(len(categories))),
        ticktext=categories,
        tickfont=dict(size=18),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Plant Height (cm)", font=dict(size=22)),
        tickfont=dict(size=18),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    showlegend=True,
    legend=dict(font=dict(size=16), yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)"),
    margin=dict(l=80, r=80, t=100, b=80),
)

# Color scheme: Python Blue first, then Python Yellow, then colorblind-safe
colors = ["#306998", "#FFD43B", "#E15759", "#76B7B2", "#59A14F"]
for i, trace in enumerate(fig.data):
    trace.marker.color = colors[i % len(colors)]

# Save as PNG (4800 x 2700 px via scale)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
