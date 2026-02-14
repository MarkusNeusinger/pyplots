"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotly 6.5.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import numpy as np
import plotly.graph_objects as go


# Data: Study hours vs exam scores (realistic educational context)
np.random.seed(42)
n_students = 120
study_hours = np.random.uniform(1, 10, n_students)
exam_scores = 45 + study_hours * 5 + np.random.randn(n_students) * 8
exam_scores = np.clip(exam_scores, 0, 100)

# Inject a few outliers to show scatter plot's outlier-detection value
study_hours[0], exam_scores[0] = 8.5, 52.0  # High effort, low result
study_hours[1], exam_scores[1] = 2.0, 78.0  # Low effort, high result
study_hours[2], exam_scores[2] = 9.2, 55.0  # Another underperformer

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=study_hours,
        y=exam_scores,
        mode="markers",
        marker={"size": 14, "color": "#306998", "opacity": 0.7, "line": {"width": 1, "color": "white"}},
        hovertemplate=("<b>Student</b><br>Study hours: %{x:.1f} h<br>Exam score: %{y:.1f}%<extra></extra>"),
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
        "gridcolor": "rgba(0,0,0,0.15)",
    },
    yaxis={
        "title": {"text": "Exam Score (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.15)",
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 80, "b": 80},
    hoverlabel={"bgcolor": "white", "font_size": 14, "font_color": "#306998"},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
