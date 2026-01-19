""" pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: plotly 6.5.2 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-19
"""

import numpy as np
import plotly.graph_objects as go


# Data - Simulated CPU usage with realistic fluctuations
np.random.seed(42)
current_value = 67  # Current CPU usage percentage
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green/Yellow/Red boundaries

# Previous values for motion blur effect (showing dynamic nature)
previous_values = [62, 65, 64, 67]  # Last few readings showing smooth transitions

# Create gauge figure
fig = go.Figure()

# Add main gauge indicator
fig.add_trace(
    go.Indicator(
        mode="gauge+number+delta",
        value=current_value,
        delta={"reference": previous_values[-2], "valueformat": ".0f", "suffix": "%"},
        number={"font": {"size": 72}, "suffix": "%"},
        title={"text": "CPU Usage", "font": {"size": 32}},
        gauge={
            "axis": {
                "range": [min_value, max_value],
                "tickwidth": 3,
                "tickcolor": "#333333",
                "tickfont": {"size": 20},
                "tickmode": "array",
                "tickvals": [0, 25, 50, 75, 100],
                "ticktext": ["0%", "25%", "50%", "75%", "100%"],
            },
            "bar": {"color": "#306998", "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 3,
            "bordercolor": "#333333",
            "steps": [
                {"range": [0, thresholds[0]], "color": "#2ecc71"},  # Green zone
                {"range": [thresholds[0], thresholds[1]], "color": "#f1c40f"},  # Yellow zone
                {"range": [thresholds[1], 100], "color": "#e74c3c"},  # Red zone
            ],
            "threshold": {"line": {"color": "#306998", "width": 6}, "thickness": 0.85, "value": current_value},
        },
        domain={"x": [0.1, 0.9], "y": [0.15, 0.9]},
    )
)

# Add annotations for min/max labels and dynamic indicator
fig.add_annotation(
    x=0.1,
    y=0.08,
    text=f"Min: {min_value}%",
    font=dict(size=20, color="#666666"),
    showarrow=False,
    xref="paper",
    yref="paper",
)

fig.add_annotation(
    x=0.9,
    y=0.08,
    text=f"Max: {max_value}%",
    font=dict(size=20, color="#666666"),
    showarrow=False,
    xref="paper",
    yref="paper",
)

# Add visual indication of real-time updates (ghost needles showing recent positions)
# This is represented by the delta showing change from previous value

fig.add_annotation(
    x=0.5,
    y=0.02,
    text="◉ Live Updating (1-5s intervals)",
    font=dict(size=18, color="#306998"),
    showarrow=False,
    xref="paper",
    yref="paper",
)

# Layout with proper sizing for 4800x2700
fig.update_layout(
    title=dict(text="gauge-realtime · plotly · pyplots.ai", font=dict(size=28), x=0.5, y=0.98, xanchor="center"),
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=50, r=50, t=80, b=50),
)

# Save as PNG (4800x2700 via scale)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs="cdn")
