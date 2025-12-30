""" pyplots.ai
bar-sorted: Sorted Bar Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Monthly sales by product category (realistic business scenario)
np.random.seed(42)
categories = [
    "Electronics",
    "Clothing",
    "Home & Garden",
    "Sports",
    "Books",
    "Toys",
    "Beauty",
    "Food & Grocery",
    "Automotive",
    "Office Supplies",
]
values = np.array([450, 380, 320, 280, 250, 220, 195, 170, 140, 95])

# Sort by value descending
sorted_indices = np.argsort(values)[::-1]
sorted_categories = [categories[i] for i in sorted_indices]
sorted_values = values[sorted_indices]

# Create figure with horizontal bars (better for labels)
fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=sorted_categories,
        x=sorted_values,
        orientation="h",
        marker=dict(
            color="#306998",  # Python Blue
            line=dict(color="#1e4d6b", width=1.5),
        ),
        text=sorted_values,
        textposition="outside",
        textfont=dict(size=18),
    )
)

# Layout for 4800x2700 px
fig.update_layout(
    title=dict(text="bar-sorted · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="Sales (thousands USD)", font=dict(size=24)),
        tickfont=dict(size=18),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
        showgrid=True,
        range=[0, max(sorted_values) * 1.15],  # Extra space for labels
    ),
    yaxis=dict(
        title=dict(text="Product Category", font=dict(size=24)),
        tickfont=dict(size=18),
        autorange="reversed",  # Largest at top
    ),
    template="plotly_white",
    margin=dict(l=180, r=80, t=100, b=80),
    bargap=0.25,
)

# Save as PNG (4800x2700 using scale=3)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
