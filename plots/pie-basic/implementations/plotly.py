"""pyplots.ai
pie-basic: Basic Pie Chart
Library: plotly 6.5.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

import plotly.graph_objects as go


# Data - Market share of cloud providers
categories = ["AWS", "Azure", "Google Cloud", "Alibaba", "IBM", "Others"]
values = [31, 24, 11, 4, 3, 27]

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1A3", "#C5A3FF"]

# Create pie chart
fig = go.Figure(
    data=[
        go.Pie(
            labels=categories,
            values=values,
            textinfo="percent+label",
            textfont={"size": 20},
            hovertemplate="%{label}<br>%{value}% market share<br>(%{percent})<extra></extra>",
            marker={"colors": colors, "line": {"color": "white", "width": 2}},
            pull=[0.05, 0, 0, 0, 0, 0],
            sort=False,
        )
    ]
)

# Layout
fig.update_layout(
    title={"text": "pie-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    legend={"font": {"size": 18}, "orientation": "v", "yanchor": "middle", "y": 0.5, "xanchor": "left", "x": 1.02},
    template="plotly_white",
    margin={"t": 100, "b": 50, "l": 20, "r": 180},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
