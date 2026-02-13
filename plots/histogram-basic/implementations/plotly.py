"""pyplots.ai
histogram-basic: Basic Histogram
Library: plotly 6.5.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-13
"""

import numpy as np
import plotly.graph_objects as go


# Data - simulating exam score distribution with realistic patterns
np.random.seed(42)
scores_main = np.random.normal(loc=72, scale=10, size=180)
scores_high = np.random.normal(loc=88, scale=5, size=40)
scores_low = np.random.normal(loc=45, scale=4, size=15)  # Struggling students / outliers
values = np.concatenate([scores_main, scores_high, scores_low])
values = np.clip(values, 0, 100)  # Exam scores between 0-100

# Create histogram with hover template for interactive HTML
fig = go.Figure()
fig.add_trace(
    go.Histogram(
        x=values,
        nbinsx=20,
        marker={"color": "#306998", "line": {"color": "white", "width": 1.5}},
        opacity=0.9,
        hovertemplate="Score: %{x:.0f}<br>Count: %{y}<extra></extra>",
    )
)

# Layout for 4800x2700 px
fig.update_layout(
    title={
        "text": "histogram-basic \u00b7 plotly \u00b7 pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Score (points)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.15)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Frequency (count)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.15)",
        "gridwidth": 1,
        "rangemode": "tozero",
    },
    template="plotly_white",
    bargap=0,
    margin={"l": 80, "r": 50, "t": 80, "b": 80},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
