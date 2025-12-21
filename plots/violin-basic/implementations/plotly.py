""" pyplots.ai
violin-basic: Basic Violin Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import numpy as np
import plotly.graph_objects as go


# Data - 4 categories with different distributions
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = {
    "Engineering": np.random.normal(85000, 12000, 200),
    "Marketing": np.random.normal(72000, 10000, 180),
    "Sales": np.random.normal(78000, 18000, 220),
    "Support": np.random.normal(55000, 8000, 190),
}

# Colors
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]

# Create figure
fig = go.Figure()

for i, (cat, values) in enumerate(data.items()):
    fig.add_trace(
        go.Violin(
            y=values,
            name=cat,
            box_visible=True,
            meanline_visible=True,
            line_color=colors[i],
            fillcolor=colors[i],
            opacity=0.7,
            points=False,
            box={"visible": True, "width": 0.15, "fillcolor": "white", "line": {"color": "#333333", "width": 2}},
            meanline={"visible": True, "color": "#333333", "width": 2},
        )
    )

# Layout
fig.update_layout(
    title={"text": "violin-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Department", "font": {"size": 22}}, "tickfont": {"size": 18}},
    yaxis={
        "title": {"text": "Annual Salary ($)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "tickformat": ",.0f",
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 100, "r": 50, "t": 100, "b": 80},
)

# Update violin traces for visibility
fig.update_traces(width=0.7, spanmode="soft")

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
