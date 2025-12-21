""" pyplots.ai
gauge-basic: Basic Gauge Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import plotly.graph_objects as go


# Data
value = 72
min_value = 0
max_value = 100
thresholds = [30, 70]

# Create gauge chart
fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": "gauge-basic · plotly · pyplots.ai", "font": {"size": 28}},
        number={"font": {"size": 48}},
        gauge={
            "axis": {"range": [min_value, max_value], "tickwidth": 2, "tickcolor": "#306998", "tickfont": {"size": 18}},
            "bar": {"color": "#306998", "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#306998",
            "steps": [
                {"range": [min_value, thresholds[0]], "color": "#FF6B6B"},
                {"range": [thresholds[0], thresholds[1]], "color": "#FFD43B"},
                {"range": [thresholds[1], max_value], "color": "#4CAF50"},
            ],
            "threshold": {"line": {"color": "#306998", "width": 6}, "thickness": 0.8, "value": value},
        },
    )
)

# Layout for 4800x2700 px
fig.update_layout(
    font={"family": "Arial", "size": 18},
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"l": 50, "r": 50, "t": 100, "b": 50},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
