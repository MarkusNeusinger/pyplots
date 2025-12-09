"""
ridgeline-basic: Ridgeline Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go
from scipy import stats


# Data - Monthly temperature readings (simulating seasonal patterns)
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

# Generate temperature data with seasonal patterns
month_temps = {
    "January": np.random.normal(2, 4, 200),
    "February": np.random.normal(4, 4, 200),
    "March": np.random.normal(9, 5, 200),
    "April": np.random.normal(14, 4, 200),
    "May": np.random.normal(18, 4, 200),
    "June": np.random.normal(22, 3, 200),
    "July": np.random.normal(25, 3, 200),
    "August": np.random.normal(24, 3, 200),
    "September": np.random.normal(20, 4, 200),
    "October": np.random.normal(14, 4, 200),
    "November": np.random.normal(8, 4, 200),
    "December": np.random.normal(4, 4, 200),
}

# Color palette - gradient from cool to warm colors
colors = [
    "#306998",  # January - Python Blue
    "#3B7BA8",
    "#4A8DB5",
    "#5E9EC2",
    "#7BB0C9",
    "#9FC5D4",
    "#C4DBDE",
    "#E8D5B5",
    "#F5C48A",
    "#F9A857",
    "#F97316",  # Orange
    "#DC2626",  # December - Signal Red
]

# Create figure
fig = go.Figure()

# Calculate KDE for each month and add as filled area
x_range = np.linspace(-15, 40, 300)
spacing = 0.15  # Vertical spacing between ridges
max_density = 0  # Track max density for scaling

# First pass: calculate all KDEs and find max density
kde_results = []
for month in months:
    data = month_temps[month]
    kde = stats.gaussian_kde(data, bw_method=0.3)
    density = kde(x_range)
    kde_results.append(density)
    max_density = max(max_density, density.max())

# Scale factor for ridge height
scale_factor = spacing * 0.8 / max_density

# Second pass: add traces from bottom to top (reversed for proper layering)
for i, month in enumerate(reversed(months)):
    idx = len(months) - 1 - i
    density = kde_results[idx] * scale_factor
    y_base = idx * spacing

    # Create the filled area trace
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([x_range, x_range[::-1]]),
            y=np.concatenate([y_base + density, np.full_like(x_range, y_base)]),
            fill="toself",
            fillcolor=colors[idx],
            line={"color": "white", "width": 1.5},
            opacity=0.75,
            name=month,
            hovertemplate=f"<b>{month}</b><br>Temperature: %{{x:.1f}}°C<extra></extra>",
        )
    )

# Update layout
fig.update_layout(
    title={"text": "Monthly Temperature Distribution", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Temperature (°C)", "font": {"size": 40}},
        "tickfont": {"size": 32},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "zeroline": False,
        "range": [-12, 38],
    },
    yaxis={
        "title": {"text": "Month", "font": {"size": 40}},
        "tickfont": {"size": 32},
        "tickmode": "array",
        "tickvals": [i * spacing for i in range(len(months))],
        "ticktext": months,
        "showgrid": False,
        "zeroline": False,
    },
    showlegend=False,
    template="plotly_white",
    margin={"l": 200, "r": 100, "t": 150, "b": 100},
    plot_bgcolor="white",
    paper_bgcolor="white",
    hoverlabel={"font_size": 24},
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
