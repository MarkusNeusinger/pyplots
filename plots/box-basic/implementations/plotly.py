""" pyplots.ai
box-basic: Basic Box Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import numpy as np
import plotly.graph_objects as go


# Data - salary distributions across departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#646464"]

# Generate realistic salary data for each department
data = {
    "Engineering": np.random.normal(95000, 15000, 100),
    "Marketing": np.random.normal(75000, 12000, 80),
    "Sales": np.random.normal(70000, 20000, 120),
    "HR": np.random.normal(65000, 10000, 60),
    "Finance": np.random.normal(85000, 14000, 90),
}

# Create figure
fig = go.Figure()

for i, (category, values) in enumerate(data.items()):
    fig.add_trace(
        go.Box(
            y=values,
            name=category,
            marker_color=colors[i],
            boxpoints="outliers",
            marker={"size": 10, "opacity": 0.7},
            line={"width": 2},
        )
    )

# Layout for 4800x2700 px
fig.update_layout(
    title={"text": "box-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Department", "font": {"size": 24}}, "tickfont": {"size": 20}},
    yaxis={
        "title": {"text": "Annual Salary ($)", "font": {"size": 24}},
        "tickfont": {"size": 20},
        "tickformat": "$,.0f",
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 100, "r": 50, "t": 100, "b": 80},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
