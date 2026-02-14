""" pyplots.ai
box-basic: Basic Box Plot
Library: plotly 6.5.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import numpy as np
import plotly.graph_objects as go


# Data - salary distributions across departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
colors = ["#306998", "#E07B42", "#4B8BBE", "#8B6DAF", "#2D9B6E"]

data = {
    "Engineering": np.random.normal(95000, 15000, 100),
    "Marketing": np.random.normal(75000, 12000, 80),
    "Sales": np.random.normal(70000, 20000, 120),
    "HR": np.random.normal(65000, 10000, 60),
    "Finance": np.random.normal(85000, 14000, 90),
}

# Clip to realistic salary range
data = {k: np.clip(v, 25000, None) for k, v in data.items()}

# Plot
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
            hovertemplate=("<b>%{x}</b><br>Salary: $%{y:,.0f}<br><extra></extra>"),
        )
    )

# Layout
fig.update_layout(
    title={"text": "box-basic \u00b7 plotly \u00b7 pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
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

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
