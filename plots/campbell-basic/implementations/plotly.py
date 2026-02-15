"""pyplots.ai
campbell-basic: Campbell Diagram
Library: plotly | Python 3.13
Quality: pending | Created: 2026-02-15
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) — slight variation with speed due to gyroscopic effects
mode_1_bending = 18 + 0.0008 * speed_rpm + np.sin(speed_rpm / 1500) * 0.5
mode_2_bending = 42 - 0.0005 * speed_rpm + np.cos(speed_rpm / 2000) * 0.8
mode_1_torsional = 55 + 0.0003 * speed_rpm
mode_axial = 72 - 0.0012 * speed_rpm + np.sin(speed_rpm / 1200) * 1.2

# Engine order lines: frequency = order * speed_rpm / 60
orders = [1, 2, 3]
order_freq = {order: order * speed_hz for order in orders}

# Find critical speed intersections (engine order line crosses natural frequency curve)
modes = {
    "1st Bending": mode_1_bending,
    "2nd Bending": mode_2_bending,
    "1st Torsional": mode_1_torsional,
    "Axial": mode_axial,
}

critical_speeds = []
critical_freqs = []
for order in orders:
    eo_freq = order_freq[order]
    for _mode_name, mode_freq in modes.items():
        diff = mode_freq - eo_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            crit_rpm = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            crit_hz = crit_rpm / 60
            crit_freq = order * crit_hz
            critical_speeds.append(crit_rpm)
            critical_freqs.append(crit_freq)

# Colors
python_blue = "#306998"
mode_colors = ["#306998", "#2CA02C", "#9467BD", "#E07B39"]
eo_color = "#888888"
critical_color = "#D62728"

fig = go.Figure()

# Natural frequency curves
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    fig.add_trace(
        go.Scatter(
            x=speed_rpm,
            y=mode_freq,
            mode="lines",
            name=mode_name,
            line={"color": mode_colors[i], "width": 3},
            hovertemplate=f"<b>{mode_name}</b><br>Speed: %{{x:.0f}} RPM<br>Freq: %{{y:.1f}} Hz<extra></extra>",
        )
    )

# Engine order lines
for order in orders:
    label = f"{order}x"
    fig.add_trace(
        go.Scatter(
            x=speed_rpm,
            y=order_freq[order],
            mode="lines",
            name=f"EO {label}",
            line={"color": eo_color, "width": 2, "dash": "dash"},
            hovertemplate=f"<b>EO {label}</b><br>Speed: %{{x:.0f}} RPM<br>Freq: %{{y:.1f}} Hz<extra></extra>",
        )
    )

# Engine order line labels at the right edge
for order in orders:
    label = f"{order}x"
    fig.add_annotation(
        x=speed_rpm[-1],
        y=order_freq[order][-1],
        text=f"<b>{label}</b>",
        showarrow=False,
        xanchor="left",
        xshift=8,
        font={"size": 16, "color": eo_color, "family": "Arial, sans-serif"},
    )

# Critical speed markers
fig.add_trace(
    go.Scatter(
        x=critical_speeds,
        y=critical_freqs,
        mode="markers",
        name="Critical Speed",
        marker={"size": 14, "color": critical_color, "symbol": "diamond", "line": {"width": 2, "color": "white"}},
        hovertemplate="<b>Critical Speed</b><br>Speed: %{x:.0f} RPM<br>Freq: %{y:.1f} Hz<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={
        "text": "campbell-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#2C3E50", "family": "Arial Black, Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.95,
    },
    xaxis={
        "title": {
            "text": "Rotational Speed (RPM)",
            "font": {"size": 22, "family": "Arial, sans-serif"},
            "standoff": 12,
        },
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.06)",
        "zeroline": False,
        "range": [0, 6500],
        "dtick": 1000,
    },
    yaxis={
        "title": {"text": "Frequency (Hz)", "font": {"size": 22, "family": "Arial, sans-serif"}, "standoff": 12},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.06)",
        "zeroline": False,
        "range": [0, 110],
        "dtick": 10,
    },
    legend={
        "font": {"size": 16, "family": "Arial, sans-serif"},
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "rgba(0,0,0,0.1)",
        "borderwidth": 1,
        "x": 0.02,
        "y": 0.98,
        "xanchor": "left",
        "yanchor": "top",
    },
    template="plotly_white",
    margin={"l": 80, "r": 60, "t": 90, "b": 70},
    plot_bgcolor="white",
    paper_bgcolor="#FAFBFC",
    hoverlabel={"bgcolor": "white", "font_size": 14},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
