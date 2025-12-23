"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)

# Create sample data: monthly sales across different product categories
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
categories = ["Electronics", "Clothing", "Food", "Books", "Sports", "Home", "Beauty", "Toys"]

# Generate realistic-looking data with some patterns
values = np.random.randn(len(categories), len(months)) * 20 + 50
# Add seasonal patterns
for month_idx in [5, 6, 7]:  # Summer boost
    values[:, month_idx] += 15
for month_idx in [10, 11]:  # Holiday boost
    values[:, month_idx] += 25

# Plot
fig = go.Figure(
    data=go.Heatmap(
        z=values,
        x=months,
        y=categories,
        colorscale="RdBu_r",  # Diverging colormap
        colorbar={
            "title": {"text": "Sales ($K)", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 30,
            "len": 0.8,
        },
        text=np.round(values, 0).astype(int),
        texttemplate="%{text}",
        textfont={"size": 14},
        hoverongaps=False,
    )
)

# Layout
fig.update_layout(
    title={"text": "heatmap-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Month", "font": {"size": 24}}, "tickfont": {"size": 18}, "side": "bottom"},
    yaxis={
        "title": {"text": "Category", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "autorange": "reversed",  # Categories from top to bottom
    },
    template="plotly_white",
    margin={"l": 120, "r": 100, "t": 100, "b": 80},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
