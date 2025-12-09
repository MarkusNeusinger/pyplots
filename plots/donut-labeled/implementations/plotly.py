"""
donut-labeled: Donut Chart with Percentage Labels
Library: plotly
"""

import plotly.graph_objects as go


# Data - Budget allocation by department
categories = ["Engineering", "Marketing", "Sales", "Operations", "R&D", "HR"]
values = [35, 20, 18, 12, 10, 5]

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create donut chart
fig = go.Figure(
    data=[
        go.Pie(
            labels=categories,
            values=values,
            hole=0.55,
            marker={"colors": colors, "line": {"color": "white", "width": 2}},
            textinfo="percent",
            textfont={"size": 20, "color": "white"},
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>",
        )
    ]
)

# Layout
fig.update_layout(
    title={"text": "Department Budget Allocation", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    legend={"orientation": "h", "yanchor": "bottom", "y": -0.15, "xanchor": "center", "x": 0.5, "font": {"size": 18}},
    template="plotly_white",
    margin={"t": 80, "b": 80, "l": 40, "r": 40},
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
