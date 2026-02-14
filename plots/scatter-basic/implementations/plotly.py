""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotly 6.5.2 | Python 3.14
Quality: 88/100 | Created: 2025-12-22
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

# Compute trend line (linear regression)
coeffs = np.polyfit(study_hours, exam_scores, 1)
trend_x = np.array([0.5, 10.5])
trend_y = np.polyval(coeffs, trend_x)

# Color palette
python_blue = "#306998"
accent_orange = "#D4782F"
trend_color = "rgba(48, 105, 152, 0.45)"

# Create figure
fig = go.Figure()

# Trend line (behind markers)
fig.add_trace(
    go.Scatter(
        x=trend_x,
        y=trend_y,
        mode="lines",
        line={"color": trend_color, "width": 3, "dash": "dash"},
        showlegend=False,
        hoverinfo="skip",
    )
)

# Main scatter points
fig.add_trace(
    go.Scatter(
        x=study_hours,
        y=exam_scores,
        mode="markers",
        marker={"size": 15, "color": python_blue, "opacity": 0.65, "line": {"width": 1.5, "color": "white"}},
        showlegend=False,
        hovertemplate=("<b>Student</b><br>Study hours: %{x:.1f} h<br>Exam score: %{y:.1f}%<extra></extra>"),
    )
)

# Highlight outliers with distinct markers
outlier_x = [8.5, 2.0, 9.2]
outlier_y = [52.0, 78.0, 55.0]
fig.add_trace(
    go.Scatter(
        x=outlier_x,
        y=outlier_y,
        mode="markers",
        marker={
            "size": 18,
            "color": accent_orange,
            "opacity": 0.9,
            "line": {"width": 2, "color": "white"},
            "symbol": "diamond",
        },
        showlegend=False,
        hoverinfo="skip",
    )
)

# Annotations for outliers (data storytelling)
annotations = [
    {"x": 2.0, "y": 78.0, "text": "Low effort,<br>high score", "ax": -70, "ay": -50},
    {"x": 8.5, "y": 52.0, "text": "High effort,<br>low score", "ax": 70, "ay": 50},
]

annotation_list = []
for ann in annotations:
    annotation_list.append(
        {
            "x": ann["x"],
            "y": ann["y"],
            "text": ann["text"],
            "showarrow": True,
            "arrowhead": 2,
            "arrowsize": 1.2,
            "arrowwidth": 2,
            "arrowcolor": accent_orange,
            "ax": ann["ax"],
            "ay": ann["ay"],
            "font": {"size": 16, "color": accent_orange, "family": "Arial, sans-serif"},
            "align": "center",
            "bgcolor": "rgba(255,255,255,0.85)",
            "bordercolor": accent_orange,
            "borderwidth": 1.5,
            "borderpad": 5,
        }
    )

# Trend label
slope_text = f"r = {np.corrcoef(study_hours, exam_scores)[0, 1]:.2f}"
annotation_list.append(
    {
        "x": 9.0,
        "y": np.polyval(coeffs, 9.0) + 3,
        "text": f"<b>{slope_text}</b>",
        "showarrow": False,
        "font": {"size": 16, "color": python_blue, "family": "Arial, sans-serif"},
        "bgcolor": "rgba(255,255,255,0.8)",
        "borderpad": 4,
    }
)

# Layout with tight axis ranges for better canvas utilization
fig.update_layout(
    title={
        "text": "scatter-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#2C3E50", "family": "Arial Black, Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.95,
    },
    xaxis={
        "title": {"text": "Study Hours (h)", "font": {"size": 22, "family": "Arial, sans-serif"}, "standoff": 15},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.08)",
        "range": [0, 11],
        "zeroline": False,
        "dtick": 2,
    },
    yaxis={
        "title": {"text": "Exam Score (%)", "font": {"size": 22, "family": "Arial, sans-serif"}, "standoff": 15},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.08)",
        "range": [35, 105],
        "zeroline": False,
        "dtick": 10,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 90, "r": 50, "t": 100, "b": 80},
    annotations=annotation_list,
    plot_bgcolor="white",
    paper_bgcolor="#FAFBFC",
    hoverlabel={"bgcolor": "white", "font_size": 14, "font_color": python_blue},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
