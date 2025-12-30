""" pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - simulate raw survey responses for fruit preferences
np.random.seed(42)
categories = ["Apple", "Banana", "Orange", "Grape", "Mango", "Strawberry"]
# Generate raw categorical data with varying frequencies
weights = [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]
raw_data = np.random.choice(categories, size=500, p=weights)

# Count frequencies
df = pd.DataFrame({"Category": raw_data})
counts = df["Category"].value_counts().sort_values(ascending=False)

# Create bar chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=counts.index.tolist(),
        y=counts.values,
        marker=dict(color="#306998", line=dict(color="#1a3d5c", width=2)),
        text=counts.values,
        textposition="outside",
        textfont=dict(size=20),
    )
)

# Layout
fig.update_layout(
    title=dict(text="bar-categorical · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(title=dict(text="Fruit Category", font=dict(size=24)), tickfont=dict(size=20)),
    yaxis=dict(
        title=dict(text="Count (Frequency)", font=dict(size=24)),
        tickfont=dict(size=20),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    showlegend=False,
    margin=dict(t=120, b=80, l=100, r=60),
    bargap=0.3,
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
