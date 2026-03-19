"""pyplots.ai
histogram-capability: Process Capability Plot with Specification Limits
Library: plotly | Python 3.13
Quality: pending | Created: 2026-03-19
"""

import numpy as np
import plotly.graph_objects as go
from scipy import stats


# Data - shaft diameter measurements (mm)
np.random.seed(42)
measurements = np.random.normal(loc=10.002, scale=0.012, size=200)

lsl = 9.95
usl = 10.05
target = 10.00

mean_val = np.mean(measurements)
sigma = np.std(measurements, ddof=1)

# Capability indices
cp = (usl - lsl) / (6 * sigma)
cpk = min((usl - mean_val) / (3 * sigma), (mean_val - lsl) / (3 * sigma))

# Normal distribution curve
x_curve = np.linspace(mean_val - 4 * sigma, mean_val + 4 * sigma, 300)
y_curve = stats.norm.pdf(x_curve, mean_val, sigma)

# Plot
fig = go.Figure()

# Histogram
fig.add_trace(
    go.Histogram(
        x=measurements,
        nbinsx=25,
        marker={"color": "rgba(48, 105, 152, 0.8)", "line": {"color": "rgba(255,255,255,0.6)", "width": 1}},
        name="Measurements",
        hovertemplate="Diameter: %{x:.4f} mm<br>Count: %{y}<extra></extra>",
    )
)

# Scale the normal curve to match histogram area
bin_width = (measurements.max() - measurements.min()) / 25
scale_factor = len(measurements) * bin_width

fig.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve * scale_factor,
        mode="lines",
        line={"color": "#1a3a5c", "width": 3},
        name="Normal Fit",
        hoverinfo="skip",
    )
)

# LSL line
fig.add_shape(
    type="line", x0=lsl, x1=lsl, y0=0, y1=0.92, yref="paper", line={"color": "#c44e52", "width": 2.5, "dash": "dash"}
)
fig.add_annotation(
    x=lsl,
    y=0.94,
    yref="paper",
    text=f"LSL<br>{lsl}",
    showarrow=False,
    font={"size": 15, "color": "#c44e52"},
    align="center",
)

# USL line
fig.add_shape(
    type="line", x0=usl, x1=usl, y0=0, y1=0.92, yref="paper", line={"color": "#c44e52", "width": 2.5, "dash": "dash"}
)
fig.add_annotation(
    x=usl,
    y=0.94,
    yref="paper",
    text=f"USL<br>{usl}",
    showarrow=False,
    font={"size": 15, "color": "#c44e52"},
    align="center",
)

# Target line
fig.add_shape(
    type="line",
    x0=target,
    x1=target,
    y0=0,
    y1=0.92,
    yref="paper",
    line={"color": "#4c8c2b", "width": 2.5, "dash": "dash"},
)
fig.add_annotation(
    x=target,
    y=0.94,
    yref="paper",
    text=f"Target<br>{target}",
    showarrow=False,
    font={"size": 15, "color": "#4c8c2b"},
    align="center",
)

# Capability indices annotation
fig.add_annotation(
    x=0.98,
    y=0.82,
    xref="paper",
    yref="paper",
    text=(
        f"<b>Capability Indices</b><br>"
        f"Cp = {cp:.2f}<br>"
        f"Cpk = {cpk:.2f}<br>"
        f"<br>"
        f"μ = {mean_val:.4f} mm<br>"
        f"σ = {sigma:.4f} mm"
    ),
    showarrow=False,
    font={"size": 15, "color": "#1a1a2e"},
    align="left",
    xanchor="right",
    yanchor="top",
    bgcolor="rgba(255,255,255,0.92)",
    bordercolor="rgba(0,0,0,0.15)",
    borderwidth=1,
    borderpad=8,
)

# Layout
fig.update_layout(
    title={
        "text": "Shaft Diameter Process Capability · histogram-capability · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#1a1a2e"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
    },
    xaxis={
        "title": {"text": "Shaft Diameter (mm)", "font": {"size": 22, "color": "#333"}},
        "tickfont": {"size": 18, "color": "#555"},
        "showgrid": False,
        "zeroline": False,
        "showline": True,
        "linecolor": "#ccc",
        "linewidth": 1,
        "range": [9.935, 10.065],
    },
    yaxis={
        "title": {"text": "Frequency", "font": {"size": 22, "color": "#333"}},
        "tickfont": {"size": 18, "color": "#555"},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.07)",
        "gridwidth": 1,
        "griddash": "dot",
        "zeroline": False,
        "showline": False,
        "rangemode": "tozero",
    },
    template="plotly_white",
    bargap=0,
    plot_bgcolor="rgba(248,249,252,1)",
    paper_bgcolor="white",
    margin={"l": 75, "r": 40, "t": 65, "b": 65},
    showlegend=True,
    legend={
        "font": {"size": 16},
        "x": 0.02,
        "y": 0.78,
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "rgba(0,0,0,0.1)",
        "borderwidth": 1,
    },
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
