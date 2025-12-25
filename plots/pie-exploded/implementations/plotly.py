""" pyplots.ai
pie-exploded: Exploded Pie Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import plotly.graph_objects as go


# Data - Market share analysis with emphasis on market leader
categories = ["Company A", "Company B", "Company C", "Company D", "Company E", "Others"]
values = [35, 22, 18, 12, 8, 5]
# Explode the market leader (Company A) and the smallest segment (Others) for contrast
explode = [0.12, 0, 0, 0, 0, 0.08]

# Colors - Python Blue as primary, Yellow for emphasized slice, colorblind-safe palette
colors = [
    "#FFD43B",  # Python Yellow - emphasized (market leader)
    "#306998",  # Python Blue
    "#4A90A4",  # Muted teal
    "#6BAF7A",  # Sage green
    "#9B7BB8",  # Muted purple
    "#C4C4C4",  # Gray for "Others"
]

# Create pie chart
fig = go.Figure(
    data=[
        go.Pie(
            labels=categories,
            values=values,
            pull=explode,
            marker={"colors": colors, "line": {"color": "#FFFFFF", "width": 3}},
            textinfo="percent+label",
            textposition="outside",
            textfont={"size": 22},
            insidetextorientation="horizontal",
            hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Share: %{percent}<extra></extra>",
        )
    ]
)

# Layout
fig.update_layout(
    title={
        "text": "Market Share Analysis · pie-exploded · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.95,
    },
    showlegend=True,
    legend={
        "font": {"size": 20},
        "orientation": "v",
        "yanchor": "middle",
        "y": 0.5,
        "xanchor": "left",
        "x": 1.02,
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": "#CCCCCC",
        "borderwidth": 1,
    },
    template="plotly_white",
    margin={"l": 80, "r": 200, "t": 120, "b": 80},
    paper_bgcolor="white",
    plot_bgcolor="white",
)

# Save as PNG (3600x3600 for square pie chart)
fig.write_image("plot.png", width=1200, height=1200, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
