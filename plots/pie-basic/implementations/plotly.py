"""pyplots.ai
pie-basic: Basic Pie Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import plotly.graph_objects as go


# Data - Budget allocation by department
categories = ["Engineering", "Marketing", "Sales", "Operations", "HR"]
values = [35, 25, 20, 12, 8]

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1A3"]

# Create pie chart
fig = go.Figure(
    data=[
        go.Pie(
            labels=categories,
            values=values,
            hole=0,
            textinfo="percent+label",
            textfont={"size": 20},
            marker={"colors": colors, "line": {"color": "white", "width": 2}},
            pull=[0.05, 0, 0, 0, 0],  # Slight explosion on first slice for emphasis
        )
    ]
)

# Layout
fig.update_layout(
    title={"text": "pie-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    legend={"font": {"size": 18}, "orientation": "v", "yanchor": "middle", "y": 0.5, "xanchor": "left", "x": 1.02},
    template="plotly_white",
    margin={"t": 100, "b": 50, "l": 50, "r": 150},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
