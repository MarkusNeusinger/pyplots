"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Wind direction frequency with speed categories
np.random.seed(42)

directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
angles = np.linspace(0, 360, 16, endpoint=False)

# Wind speed categories (stacked bars)
calm = np.random.randint(5, 15, 16)
light = np.random.randint(8, 20, 16)
moderate = np.random.randint(3, 12, 16)
strong = np.random.randint(1, 8, 16)

# Create polar bar chart (wind rose)
fig = go.Figure()

# Add stacked bars for each wind speed category
fig.add_trace(go.Barpolar(r=calm, theta=angles, name="Calm (0-5 km/h)", marker_color="#306998", opacity=0.9, width=20))

fig.add_trace(
    go.Barpolar(r=light, theta=angles, name="Light (5-15 km/h)", marker_color="#FFD43B", opacity=0.9, width=20)
)

fig.add_trace(
    go.Barpolar(r=moderate, theta=angles, name="Moderate (15-25 km/h)", marker_color="#4B8BBE", opacity=0.9, width=20)
)

fig.add_trace(
    go.Barpolar(r=strong, theta=angles, name="Strong (25+ km/h)", marker_color="#646464", opacity=0.9, width=20)
)

# Layout for wind rose
fig.update_layout(
    title=dict(
        text="Wind Rose Distribution · polar-bar · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"
    ),
    polar=dict(
        radialaxis=dict(
            visible=True,
            showticklabels=True,
            tickfont=dict(size=16),
            title=dict(text="Frequency (%)", font=dict(size=18)),
            gridcolor="rgba(0,0,0,0.15)",
        ),
        angularaxis=dict(
            tickmode="array",
            tickvals=angles,
            ticktext=directions,
            tickfont=dict(size=18, color="#333333"),
            direction="clockwise",
            rotation=90,
            gridcolor="rgba(0,0,0,0.15)",
        ),
        bgcolor="rgba(255,255,255,0.9)",
    ),
    legend=dict(
        font=dict(size=18),
        x=1.05,
        y=0.5,
        xanchor="left",
        yanchor="middle",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#cccccc",
        borderwidth=1,
    ),
    template="plotly_white",
    margin=dict(l=100, r=200, t=120, b=80),
    barmode="stack",
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
