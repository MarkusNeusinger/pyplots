"""
violin-basic: Basic Violin Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - Employee performance scores grouped by department
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Generate realistic performance scores (50-100 scale) with different distributions
data = {
    "Engineering": np.random.normal(78, 8, 150),
    "Marketing": np.random.normal(75, 10, 120),
    "Sales": np.concatenate([np.random.normal(70, 6, 80), np.random.normal(85, 4, 50)]),  # Bimodal
    "HR": np.random.normal(80, 7, 100),
    "Finance": np.random.normal(82, 6, 130),
}

# Clip values to realistic range
for dept in data:
    data[dept] = np.clip(data[dept], 50, 100)

# Create figure
fig = go.Figure()

# Add violin traces for each department
for i, dept in enumerate(departments):
    fig.add_trace(
        go.Violin(
            y=data[dept],
            name=dept,
            box_visible=True,
            meanline_visible=True,
            fillcolor=colors[i],
            line_color="#1a1a1a",
            opacity=0.7,
        )
    )

# Update layout
fig.update_layout(
    title={"text": "Employee Performance Scores by Department", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    xaxis_title={"text": "Department", "font": {"size": 40}},
    yaxis_title={"text": "Performance Score", "font": {"size": 40}},
    template="plotly_white",
    showlegend=False,
    font={"size": 32},
    xaxis={"tickfont": {"size": 32}},
    yaxis={"tickfont": {"size": 32}, "range": [45, 105]},
    violinmode="group",
    margin={"l": 100, "r": 50, "t": 120, "b": 100},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
