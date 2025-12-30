"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Different product categories with varied distributions
np.random.seed(42)

categories = ["Product A", "Product B", "Product C", "Product D"]
n_per_category = 50

# Generate data with different distributions per category
data_values = {
    "Product A": np.random.normal(75, 10, n_per_category),
    "Product B": np.random.normal(60, 15, n_per_category),
    "Product C": np.concatenate(
        [np.random.normal(50, 5, n_per_category // 2), np.random.normal(80, 5, n_per_category // 2)]
    ),
    "Product D": np.random.exponential(10, n_per_category) + 40,
}

# Add outliers to demonstrate box plot whiskers
data_values["Product A"] = np.append(data_values["Product A"], [35, 105])
data_values["Product B"] = np.append(data_values["Product B"], [15, 110])

# Colors
box_color = "#306998"
point_color = "#FFD43B"

# Create figure
fig = go.Figure()

# Add box plots using Plotly's built-in boxpoints for strip overlay
for cat, values in data_values.items():
    fig.add_trace(
        go.Box(
            y=values,
            name=cat,
            boxpoints="all",
            jitter=0.4,
            pointpos=0,
            marker=dict(color=point_color, size=10, opacity=0.7, line=dict(width=1, color="#333333")),
            line=dict(width=3, color=box_color),
            fillcolor="rgba(48, 105, 152, 0.5)",
            whiskerwidth=0.8,
            showlegend=False,
            hovertemplate=f"{cat}<br>Value: %{{y:.1f}}<extra></extra>",
        )
    )

# Update layout
fig.update_layout(
    title=dict(text="cat-box-strip · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(title=dict(text="Product Category", font=dict(size=24)), tickfont=dict(size=20), showgrid=False),
    yaxis=dict(
        title=dict(text="Performance Score", font=dict(size=24)),
        tickfont=dict(size=20),
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=100, r=80, t=120, b=100),
)

# Save as PNG (4800 x 2700 px via scale=3)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
