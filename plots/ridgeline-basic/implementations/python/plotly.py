"""anyplot.ai
ridgeline-basic: Basic Ridgeline Plot
Library: plotly | Python 3.13
Quality: pending | Updated: 2026-04-30
"""

import os

import numpy as np
import plotly.graph_objects as go


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"
LINE_EDGE = "rgba(26,26,23,0.35)" if THEME == "light" else "rgba(240,239,232,0.35)"

# Data - Monthly temperature distributions (Northern hemisphere)
np.random.seed(42)

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

base_temps = [-2, 0, 5, 12, 18, 23, 26, 25, 20, 13, 6, 1]
data = {}
for i, month in enumerate(months):
    std = 4 if i in [2, 3, 8, 9] else 3
    data[month] = np.random.normal(base_temps[i], std, 200)

# X range for density evaluation
x_range = np.linspace(-15, 40, 300)

# Seasonal color gradient: cold blue → warm yellow/orange → cold blue
colors = [
    "#306998",  # January - deep blue (cold)
    "#3d78a8",  # February
    "#5298b8",  # March
    "#72b8c8",  # April
    "#94c8a0",  # May - transitioning
    "#FFD43B",  # June - warm yellow
    "#ff9f43",  # July - warm orange
    "#ff7f50",  # August - coral
    "#94c8a0",  # September - transitioning back
    "#72b8c8",  # October
    "#4a88b8",  # November
    "#306998",  # December - deep blue (cold)
]

# Plot
fig = go.Figure()

# Scaling for ridge height and ~50% overlap per spec
ridge_scale = 0.12
overlap = 0.5

# Add ridges bottom-to-top so January sits at the bottom
for i, month in enumerate(reversed(months)):
    idx = len(months) - 1 - i
    temps = data[month]

    # KDE using Silverman's rule for bandwidth selection
    n = len(temps)
    std_dev = np.std(temps, ddof=1)
    iqr = np.percentile(temps, 75) - np.percentile(temps, 25)
    bandwidth = 0.9 * min(std_dev, iqr / 1.34) * n ** (-0.2)

    density = np.zeros_like(x_range)
    for xi in temps:
        density += np.exp(-0.5 * ((x_range - xi) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    density = density / density.max() * ridge_scale
    y_offset = i * (1 - overlap) * ridge_scale
    y_fill = density + y_offset

    fig.add_trace(
        go.Scatter(
            x=np.concatenate([[x_range[0]], x_range, [x_range[-1]]]),
            y=np.concatenate([[y_offset], y_fill, [y_offset]]),
            fill="toself",
            fillcolor=colors[idx],
            line={"color": LINE_EDGE, "width": 1.5},
            mode="lines",
            name=month,
            showlegend=False,
            hovertemplate=f"{month}<br>Temperature: %{{x:.1f}}°C<extra></extra>",
        )
    )

# Y-tick positions aligned to ridge peaks
y_ticks = [(len(months) - 1 - i) * (1 - overlap) * ridge_scale + ridge_scale * 0.4 for i in range(len(months))]

# Style
fig.update_layout(
    title={"text": "ridgeline-basic · plotly · anyplot.ai", "font": {"size": 48, "color": INK}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Temperature (°C)", "font": {"size": 36, "color": INK}},
        "tickfont": {"size": 28, "color": INK_SOFT},
        "range": [-15, 40],
        "gridcolor": GRID,
        "showgrid": True,
        "zeroline": False,
        "linecolor": INK_SOFT,
    },
    yaxis={
        "title": {"text": "", "font": {"size": 36}},
        "tickfont": {"size": 28, "color": INK_SOFT},
        "tickvals": y_ticks,
        "ticktext": list(reversed(months)),
        "showgrid": False,
        "zeroline": False,
        "range": [-0.02, max(y_ticks) + ridge_scale * 0.7],
    },
    paper_bgcolor=PAGE_BG,
    plot_bgcolor=PAGE_BG,
    font={"color": INK},
    margin={"l": 180, "r": 60, "t": 120, "b": 130},
    annotations=[
        {
            "x": 0.5,
            "y": -0.10,
            "xref": "paper",
            "yref": "paper",
            "text": "Color encodes seasonal temperature: ❄ Cold (blue) → ☀ Warm (orange/yellow) → ❄ Cold (blue)",
            "showarrow": False,
            "font": {"size": 20, "color": INK_SOFT},
            "align": "center",
        }
    ],
)

# Save
fig.write_image(f"plot-{THEME}.png", width=1600, height=900, scale=3)
fig.write_html(f"plot-{THEME}.html", include_plotlyjs="cdn")
