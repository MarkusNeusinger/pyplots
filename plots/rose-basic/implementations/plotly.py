""" pyplots.ai
rose-basic: Basic Rose Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import plotly.graph_objects as go


# Data - Monthly rainfall (mm) showing seasonal pattern
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 62, 55, 48, 42, 38, 35, 40, 52, 68, 82, 85]

# Calculate angles - starting at top (12 o'clock) going clockwise
n_categories = len(months)
angle_width = 360 / n_categories
# Plotly uses degrees, starting from 3 o'clock position going counter-clockwise
# To start at 12 o'clock and go clockwise, we adjust the theta values
theta = [(90 - i * angle_width) % 360 for i in range(n_categories)]

# Create the rose chart using barpolar
fig = go.Figure()

fig.add_trace(
    go.Barpolar(
        r=rainfall,
        theta=theta,
        width=[angle_width] * n_categories,
        marker={
            "color": rainfall,
            "colorscale": [[0, "#FFD43B"], [1, "#306998"]],  # Python Yellow to Blue
            "line": {"color": "white", "width": 2},
            "cmin": min(rainfall),
            "cmax": max(rainfall),
        },
        text=months,
        hovertemplate="<b>%{text}</b><br>Rainfall: %{r} mm<extra></extra>",
    )
)

# Update layout for 4800x2700 px output
fig.update_layout(
    title={"text": "rose-basic · plotly · pyplots.ai", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    template="plotly_white",
    polar={
        "angularaxis": {
            "tickmode": "array",
            "tickvals": theta,
            "ticktext": months,
            "tickfont": {"size": 28},
            "direction": "clockwise",
            "rotation": 90,  # Start at top
            "gridcolor": "rgba(0,0,0,0.1)",
            "linecolor": "rgba(0,0,0,0.3)",
        },
        "radialaxis": {
            "tickfont": {"size": 22},
            "gridcolor": "rgba(0,0,0,0.15)",
            "linecolor": "rgba(0,0,0,0.3)",
            "ticksuffix": " mm",
            "angle": 45,
            "dtick": 20,
        },
        "bgcolor": "white",
    },
    showlegend=False,
    margin={"l": 100, "r": 100, "t": 150, "b": 100},
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs="cdn")
