""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotly 6.5.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import numpy as np
import plotly.graph_objects as go


# Data: Coffee consumption vs afternoon productivity (office setting)
np.random.seed(42)
n = 120
cups_of_coffee = np.random.uniform(0.5, 6, n)
productivity = 55 + cups_of_coffee * 6 + np.random.randn(n) * 9
productivity = np.clip(productivity, 20, 100)

# Add a few deliberate outliers for scatter demonstration
outlier_x = np.array([1.0, 5.5, 3.2, 0.8])
outlier_y = np.array([92, 48, 95, 78])
cups_of_coffee = np.concatenate([cups_of_coffee, outlier_x])
productivity = np.concatenate([productivity, outlier_y])

# Color by productivity score for visual depth
colors = productivity.copy()

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=cups_of_coffee,
        y=productivity,
        mode="markers",
        marker={
            "size": 14,
            "color": colors,
            "colorscale": [[0.0, "#4a1486"], [0.25, "#6a51a3"], [0.5, "#807dba"], [0.75, "#54a0c2"], [1.0, "#2db87d"]],
            "opacity": 0.75,
            "line": {"width": 1, "color": "rgba(255,255,255,0.6)"},
            "colorbar": {
                "title": {"text": "Score", "font": {"size": 18}},
                "tickfont": {"size": 16},
                "thickness": 18,
                "len": 0.6,
            },
        },
        hovertemplate=("<b>%{x:.1f} cups</b><br>Productivity: %{y:.0f}%<extra></extra>"),
    )
)

# Layout
fig.update_layout(
    title={
        "text": "scatter-basic \u00b7 plotly \u00b7 pyplots.ai",
        "font": {"size": 28, "color": "#2d2d2d"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Daily Coffee Intake (cups)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.2)",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Afternoon Productivity (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.2)",
        "zeroline": False,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 100, "t": 80, "b": 80},
    plot_bgcolor="rgba(248,248,252,1)",
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
