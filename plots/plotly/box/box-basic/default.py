"""
box-basic: Basic Box Plot
Library: plotly
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create figure
fig = go.Figure()

# Add box trace for each group
for i, group in enumerate(["A", "B", "C", "D"]):
    group_data = data[data["group"] == group]["value"]
    fig.add_trace(
        go.Box(y=group_data, name=f"Group {group}", marker_color=colors[i], boxpoints="outliers", line_width=2)
    )

# Layout
fig.update_layout(
    title={"text": "Basic Box Plot", "font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    xaxis_title={"text": "Group", "font": {"size": 32}},
    yaxis_title={"text": "Value", "font": {"size": 32}},
    template="plotly_white",
    showlegend=False,
    font={"size": 26},
    xaxis={"tickfont": {"size": 26}},
    yaxis={"tickfont": {"size": 26}, "gridwidth": 1, "gridcolor": "rgba(0,0,0,0.1)"},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
