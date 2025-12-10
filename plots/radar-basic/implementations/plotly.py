"""
radar-basic: Basic Radar Chart
Library: plotly
"""

import plotly.graph_objects as go


# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 70, 90, 75, 80]
athlete_b = [70, 85, 75, 90, 70]

# Close the polygon by repeating the first value
categories_closed = categories + [categories[0]]
athlete_a_closed = athlete_a + [athlete_a[0]]
athlete_b_closed = athlete_b + [athlete_b[0]]

# Create figure
fig = go.Figure()

# Add trace for Athlete A
fig.add_trace(
    go.Scatterpolar(
        r=athlete_a_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(48, 105, 152, 0.3)",
        line={"color": "#306998", "width": 2},
        name="Athlete A",
    )
)

# Add trace for Athlete B
fig.add_trace(
    go.Scatterpolar(
        r=athlete_b_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(255, 212, 59, 0.3)",
        line={"color": "#FFD43B", "width": 2},
        name="Athlete B",
    )
)

# Update layout
fig.update_layout(
    title={"text": "Athlete Performance Comparison", "font": {"size": 32}, "x": 0.5},
    polar={
        "radialaxis": {"visible": True, "range": [0, 100], "tickfont": {"size": 16}, "gridcolor": "rgba(0, 0, 0, 0.1)"},
        "angularaxis": {"tickfont": {"size": 20}, "gridcolor": "rgba(0, 0, 0, 0.1)"},
        "bgcolor": "white",
    },
    legend={"font": {"size": 16}, "x": 0.95, "y": 0.95, "xanchor": "right", "yanchor": "top"},
    showlegend=True,
    template="plotly_white",
    margin={"l": 100, "r": 100, "t": 100, "b": 100},
)

# Save as PNG (4800 × 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
