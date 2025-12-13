"""
bar-basic: Basic Bar Chart
Library: plotly
"""

import plotly.graph_objects as go


# Data
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Automotive", "Health"]
values = [45200, 38700, 31500, 27800, 24300, 21600, 18900, 15400]

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker_color="#306998",
        text=values,
        textposition="outside",
        texttemplate="%{text:,.0f}",
        textfont={"size": 32},
    )
)

# Layout
fig.update_layout(
    title={"text": "Sales by Product Category", "font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Product Category", "font": {"size": 40}}, "tickfont": {"size": 32}},
    yaxis={
        "title": {"text": "Sales ($)", "font": {"size": 40}},
        "tickfont": {"size": 32},
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    template="plotly_white",
    bargap=0.3,
    margin={"t": 120, "b": 80, "l": 100, "r": 50},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
