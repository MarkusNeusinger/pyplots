"""pyplots.ai
campbell-basic: Campbell Diagram
Library: plotly 6.5.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-02-15
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) — variation with speed due to gyroscopic effects
mode_1_bending = 18 + 0.002 * speed_rpm + np.sin(speed_rpm / 1500) * 0.8
mode_2_bending = 45 - 0.0018 * speed_rpm + np.cos(speed_rpm / 2000) * 1.0
mode_1_torsional = 55 + 0.0003 * speed_rpm
mode_axial = 72 - 0.0025 * speed_rpm + np.sin(speed_rpm / 1200) * 1.5

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
critical_modes = []
for order in orders:
    eo_freq = order_freq[order]
    for mode_name, mode_freq in modes.items():
        diff = mode_freq - eo_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            crit_rpm = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            crit_hz = crit_rpm / 60
            crit_freq = order * crit_hz
            critical_speeds.append(crit_rpm)
            critical_freqs.append(crit_freq)
            critical_modes.append(f"{mode_name} × EO {order}x")

# Colorblind-safe palette (avoids red-green confusion)
mode_colors = ["#306998", "#D4A017", "#9467BD", "#E07B39"]
eo_color = "#7F7F7F"
critical_color = "#C44E52"

fig = go.Figure()

# Subtle shaded bands at critical speed zones
for cs_rpm in critical_speeds:
    fig.add_vrect(x0=cs_rpm - 80, x1=cs_rpm + 80, fillcolor="rgba(196, 78, 82, 0.04)", line_width=0, layer="below")

# Natural frequency curves with varying line styles for extra distinction
line_dashes = ["solid", "solid", "solid", "solid"]
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    fig.add_trace(
        go.Scatter(
            x=speed_rpm,
            y=mode_freq,
            mode="lines",
            name=mode_name,
            line={"color": mode_colors[i], "width": 3.5, "dash": line_dashes[i]},
            hovertemplate=(f"<b>{mode_name}</b><br>Speed: %{{x:.0f}} RPM<br>Freq: %{{y:.1f}} Hz<extra></extra>"),
        )
    )

# Engine order lines (clipped to visible y-axis range)
y_max = 110
for order in orders:
    label = f"{order}x"
    eo_y = order_freq[order]
    mask = eo_y <= y_max
    fig.add_trace(
        go.Scatter(
            x=speed_rpm[mask],
            y=eo_y[mask],
            mode="lines",
            name=f"EO {label}",
            line={"color": eo_color, "width": 1.8, "dash": "dash"},
            hovertemplate=(f"<b>EO {label}</b><br>Speed: %{{x:.0f}} RPM<br>Freq: %{{y:.1f}} Hz<extra></extra>"),
        )
    )

# Engine order labels placed at top of visible portion
for order in orders:
    label = f"{order}x"
    eo_y = order_freq[order]
    visible_mask = eo_y <= y_max
    if np.any(visible_mask):
        last_visible_idx = np.where(visible_mask)[0][-1]
        ann_x = speed_rpm[last_visible_idx]
        ann_y = eo_y[last_visible_idx]
    else:
        ann_x = speed_rpm[-1]
        ann_y = y_max
    fig.add_annotation(
        x=ann_x,
        y=ann_y,
        text=f"<b>{label}</b>",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        xshift=6,
        yshift=-2,
        font={"size": 16, "color": eo_color, "family": "Arial, sans-serif"},
    )

# Critical speed markers with descriptive hover
fig.add_trace(
    go.Scatter(
        x=critical_speeds,
        y=critical_freqs,
        mode="markers",
        name="Critical Speed",
        marker={"size": 14, "color": critical_color, "symbol": "diamond", "line": {"width": 2, "color": "white"}},
        customdata=critical_modes,
        hovertemplate=(
            "<b>Critical Speed</b><br>%{customdata}<br>Speed: %{x:.0f} RPM<br>Freq: %{y:.1f} Hz<extra></extra>"
        ),
    )
)

# Layout
fig.update_layout(
    title={
        "text": "campbell-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#1A2A3A", "family": "Arial Black, Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
    },
    xaxis={
        "title": {
            "text": "Rotational Speed (RPM)",
            "font": {"size": 22, "color": "#333", "family": "Arial, sans-serif"},
            "standoff": 12,
        },
        "tickfont": {"size": 18, "color": "#444"},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.05)",
        "zeroline": False,
        "range": [0, 6500],
        "dtick": 1000,
        "showline": True,
        "linewidth": 1.5,
        "linecolor": "#CCC",
        "mirror": False,
    },
    yaxis={
        "title": {
            "text": "Frequency (Hz)",
            "font": {"size": 22, "color": "#333", "family": "Arial, sans-serif"},
            "standoff": 12,
        },
        "tickfont": {"size": 18, "color": "#444"},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.05)",
        "zeroline": False,
        "range": [0, y_max],
        "dtick": 10,
        "showline": True,
        "linewidth": 1.5,
        "linecolor": "#CCC",
        "mirror": False,
    },
    legend={
        "font": {"size": 15, "family": "Arial, sans-serif", "color": "#333"},
        "bgcolor": "rgba(255,255,255,0.92)",
        "bordercolor": "rgba(0,0,0,0.08)",
        "borderwidth": 1,
        "x": 0.01,
        "y": 0.99,
        "xanchor": "left",
        "yanchor": "top",
        "tracegroupgap": 2,
        "itemsizing": "constant",
    },
    template="plotly_white",
    margin={"l": 80, "r": 70, "t": 90, "b": 70},
    plot_bgcolor="white",
    paper_bgcolor="#F8F9FA",
    hoverlabel={"bgcolor": "white", "font_size": 14, "bordercolor": "#DDD"},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
