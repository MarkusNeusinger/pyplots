"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-22
"""

import numpy as np
import plotly.graph_objects as go


# Data: Study hours vs exam scores (realistic educational context)
np.random.seed(42)
study_hours = np.random.uniform(1, 10, 100)
exam_scores = 45 + study_hours * 5 + np.random.randn(100) * 8
exam_scores = np.clip(exam_scores, 0, 100)

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=study_hours,
        y=exam_scores,
        mode="markers",
        marker={"size": 16, "color": "#306998", "opacity": 0.7},
        hovertemplate="Hours: %{x:.1f}<br>Score: %{y:.1f}<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={"text": "scatter-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Study Hours (h)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    yaxis={
        "title": {"text": "Exam Score (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 80, "b": 80},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
