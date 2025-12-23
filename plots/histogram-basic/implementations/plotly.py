""" pyplots.ai
histogram-basic: Basic Histogram
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data - simulating exam score distribution with realistic patterns
np.random.seed(42)
# Mix of normal distributions to show interesting histogram features
scores_main = np.random.normal(loc=72, scale=10, size=180)
scores_high = np.random.normal(loc=88, scale=5, size=40)
values = np.concatenate([scores_main, scores_high])
values = np.clip(values, 0, 100)  # Exam scores between 0-100

# Create histogram
fig = go.Figure()
fig.add_trace(
    go.Histogram(
        x=values, nbinsx=20, marker={"color": "#306998", "line": {"color": "white", "width": 1.5}}, opacity=0.9
    )
)

# Layout for 4800x2700 px
fig.update_layout(
    title={"text": "histogram-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Score (points)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Frequency (count)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
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
