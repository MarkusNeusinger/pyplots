"""pyplots.ai
polar-line: Polar Line Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Monthly average temperatures (cyclical pattern)
np.random.seed(42)
months = np.arange(0, 360, 30)  # 12 months as degrees (0, 30, 60, ..., 330)
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# City A - Northern hemisphere pattern (warm summer, cold winter)
city_a_temps = np.array([2, 4, 10, 15, 20, 25, 28, 27, 22, 15, 8, 3])

# City B - Southern hemisphere pattern (inverted seasons)
city_b_temps = np.array([26, 25, 22, 17, 12, 8, 7, 9, 13, 18, 22, 25])

# Close the loop by appending first value
theta_closed = np.append(months, months[0])
city_a_closed = np.append(city_a_temps, city_a_temps[0])
city_b_closed = np.append(city_b_temps, city_b_temps[0])

# Create figure
fig = go.Figure()

# Add City A trace (Python Blue)
fig.add_trace(
    go.Scatterpolar(
        r=city_a_closed,
        theta=theta_closed,
        mode="lines+markers",
        name="City A (Northern)",
        line={"color": "#306998", "width": 4},
        marker={"size": 14, "color": "#306998"},
        fill="toself",
        fillcolor="rgba(48, 105, 152, 0.15)",
    )
)

# Add City B trace (Python Yellow)
fig.add_trace(
    go.Scatterpolar(
        r=city_b_closed,
        theta=theta_closed,
        mode="lines+markers",
        name="City B (Southern)",
        line={"color": "#FFD43B", "width": 4},
        marker={"size": 14, "color": "#FFD43B", "line": {"color": "#333", "width": 1}},
        fill="toself",
        fillcolor="rgba(255, 212, 59, 0.15)",
    )
)

# Update layout
fig.update_layout(
    title={
        "text": "Monthly Temperature Patterns · polar-line · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333"},
        "x": 0.5,
        "xanchor": "center",
    },
    polar={
        "radialaxis": {
            "visible": True,
            "range": [0, 35],
            "tickfont": {"size": 18},
            "title": {"text": "Temperature (°C)", "font": {"size": 20}},
            "gridcolor": "rgba(0, 0, 0, 0.1)",
            "gridwidth": 1,
        },
        "angularaxis": {
            "tickmode": "array",
            "tickvals": months,
            "ticktext": month_labels,
            "tickfont": {"size": 20},
            "direction": "clockwise",
            "rotation": 90,
            "gridcolor": "rgba(0, 0, 0, 0.15)",
            "gridwidth": 1,
        },
        "bgcolor": "rgba(255, 255, 255, 1)",
    },
    legend={
        "font": {"size": 20},
        "x": 0.98,
        "y": 0.98,
        "xanchor": "right",
        "yanchor": "top",
        "bgcolor": "rgba(255, 255, 255, 0.9)",
        "bordercolor": "rgba(0, 0, 0, 0.2)",
        "borderwidth": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 100, "t": 120, "b": 80},
)

# Save as PNG (4800 x 2700 px using scale=3)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
