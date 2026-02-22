"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: plotly 6.5.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-22
"""

import plotly.graph_objects as go


# Data - Multiple KPIs with different performance levels
metrics = [
    {"label": "Revenue ($K)", "actual": 275, "target": 250, "ranges": [150, 200, 300]},
    {"label": "Profit ($K)", "actual": 85, "target": 100, "ranges": [50, 75, 125]},
    {"label": "Customers", "actual": 320, "target": 400, "ranges": [200, 350, 500]},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "ranges": [3.0, 4.0, 5.0]},
]

# Grayscale colors for qualitative ranges (poor -> satisfactory -> good)
range_colors = ["#A6A6A6", "#C0C0C0", "#DCDCDC"]

# Create figure with native Indicator traces (bullet mode)
fig = go.Figure()
n = len(metrics)
spacing = 0.04
row_height = (1.0 - spacing * (n - 1)) / n

for i, m in enumerate(metrics):
    y_start = 1.0 - (i + 1) * row_height - i * spacing
    y_end = y_start + row_height

    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=m["actual"],
            number={"font": {"size": 26, "color": "#306998"}},
            domain={"x": [0.18, 0.95], "y": [y_start, y_end]},
            title={"text": m["label"], "font": {"size": 22}, "align": "left"},
            gauge={
                "shape": "bullet",
                "axis": {"range": [0, m["ranges"][-1]], "tickfont": {"size": 16}},
                "bar": {"color": "#306998"},
                "bgcolor": "white",
                "threshold": {"line": {"color": "#1A1A1A", "width": 4}, "thickness": 0.75, "value": m["target"]},
                "steps": [
                    {"range": [0, m["ranges"][0]], "color": range_colors[0]},
                    {"range": [m["ranges"][0], m["ranges"][1]], "color": range_colors[1]},
                    {"range": [m["ranges"][1], m["ranges"][2]], "color": range_colors[2]},
                ],
            },
        )
    )

# Layout
fig.update_layout(
    title={"text": "bullet-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    template="plotly_white",
    margin={"l": 40, "r": 40, "t": 100, "b": 40},
    height=900,
    width=1600,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
