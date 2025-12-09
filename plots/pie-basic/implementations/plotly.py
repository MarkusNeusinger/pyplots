"""
pie-basic: Basic Pie Chart
Library: plotly
"""

import pandas as pd
import plotly.graph_objects as go


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Create plot
fig = go.Figure(
    data=[
        go.Pie(
            labels=data["category"],
            values=data["value"],
            marker={"colors": colors, "line": {"color": "white", "width": 2}},
            textinfo="label+percent",
            textfont={"size": 16},
            textposition="inside",
            insidetextorientation="horizontal",
            hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>",
            rotation=90,
        )
    ]
)

# Layout
fig.update_layout(
    title={"text": "Basic Pie Chart", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    legend={"font": {"size": 16}, "orientation": "v", "yanchor": "middle", "y": 0.5, "xanchor": "left", "x": 1.02},
    template="plotly_white",
    margin={"l": 50, "r": 150, "t": 80, "b": 50},
)

# Save (4800 x 2700 px using scale=3 with 1600x900 base)
fig.write_image("plot.png", width=1600, height=900, scale=3)
