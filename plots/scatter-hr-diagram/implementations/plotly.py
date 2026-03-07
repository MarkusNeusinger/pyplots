"""pyplots.ai
scatter-hr-diagram: Hertzsprung-Russell Diagram
Library: plotly | Python 3.13
Quality: pending | Created: 2026-03-07
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)

# Spectral type temperature ranges and colors
spectral_config = {
    "O": {"temp": (30000, 40000), "color": "#6B93D6", "n": 15},
    "B": {"temp": (10000, 30000), "color": "#9BB0FF", "n": 40},
    "A": {"temp": (7500, 10000), "color": "#CAD7FF", "n": 45},
    "F": {"temp": (6000, 7500), "color": "#F8F7FF", "n": 50},
    "G": {"temp": (5200, 6000), "color": "#FFF4EA", "n": 55},
    "K": {"temp": (3700, 5200), "color": "#FFD2A1", "n": 50},
    "M": {"temp": (2400, 3700), "color": "#FFCC6F", "n": 45},
}

temperatures = []
luminosities = []
spectral_types = []
regions = []

# Main sequence stars (L ~ T^4 relationship with scatter)
for stype, cfg in spectral_config.items():
    n = cfg["n"]
    temp = np.random.uniform(cfg["temp"][0], cfg["temp"][1], n)
    log_lum_base = 4.0 * np.log10(temp / 5778)
    log_lum = log_lum_base + np.random.normal(0, 0.3, n)
    temperatures.extend(temp)
    luminosities.extend(10**log_lum)
    spectral_types.extend([stype] * n)
    regions.extend(["Main Sequence"] * n)

# Red giants (cool but bright)
n_rg = 35
rg_temp = np.random.uniform(3000, 5200, n_rg)
rg_lum = 10 ** np.random.uniform(1.5, 3.5, n_rg)
temperatures.extend(rg_temp)
luminosities.extend(rg_lum)
spectral_types.extend(np.where(rg_temp > 3700, "K", "M").tolist())
regions.extend(["Red Giants"] * n_rg)

# Supergiants (bright across temperatures)
n_sg = 20
sg_temp = np.random.uniform(3500, 30000, n_sg)
sg_lum = 10 ** np.random.uniform(4.0, 5.8, n_sg)
temperatures.extend(sg_temp)
luminosities.extend(sg_lum)
sg_types = []
for t in sg_temp:
    if t > 30000:
        sg_types.append("O")
    elif t > 10000:
        sg_types.append("B")
    elif t > 7500:
        sg_types.append("A")
    elif t > 6000:
        sg_types.append("F")
    elif t > 5200:
        sg_types.append("G")
    elif t > 3700:
        sg_types.append("K")
    else:
        sg_types.append("M")
spectral_types.extend(sg_types)
regions.extend(["Supergiants"] * n_sg)

# White dwarfs (hot but dim)
n_wd = 30
wd_temp = np.random.uniform(7000, 30000, n_wd)
wd_lum = 10 ** np.random.uniform(-4, -1.5, n_wd)
temperatures.extend(wd_temp)
luminosities.extend(wd_lum)
wd_types = []
for t in wd_temp:
    if t > 10000:
        wd_types.append("B")
    elif t > 7500:
        wd_types.append("A")
    else:
        wd_types.append("F")
spectral_types.extend(wd_types)
regions.extend(["White Dwarfs"] * n_wd)

temperatures = np.array(temperatures)
luminosities = np.array(luminosities)
spectral_types = np.array(spectral_types)
regions = np.array(regions)

# Color map for spectral types (conventional astronomical colors)
spectral_colors = {
    "O": "#6B93D6",
    "B": "#9BB0FF",
    "A": "#CAD7FF",
    "F": "#F8F7FF",
    "G": "#FFF4EA",
    "K": "#FFD2A1",
    "M": "#FFCC6F",
}

# Plot
fig = go.Figure()

spectral_order = ["O", "B", "A", "F", "G", "K", "M"]
for stype in spectral_order:
    mask = spectral_types == stype
    fig.add_trace(
        go.Scatter(
            x=temperatures[mask],
            y=luminosities[mask],
            mode="markers",
            name=f"Type {stype}",
            marker=dict(size=10, color=spectral_colors[stype], line=dict(width=1, color="#333333"), opacity=0.85),
            hovertemplate=(
                f"Spectral Type: {stype}<br>Temperature: %{{x:,.0f}} K<br>Luminosity: %{{y:.4g}} L☉<br><extra></extra>"
            ),
        )
    )

# Sun reference point
fig.add_trace(
    go.Scatter(
        x=[5778],
        y=[1.0],
        mode="markers+text",
        name="Sun",
        text=["☉ Sun"],
        textposition="top right",
        textfont=dict(size=18, color="#E8A317"),
        marker=dict(size=18, color="#FDB813", line=dict(width=2, color="#E8A317"), symbol="star"),
        hovertemplate=("The Sun<br>Temperature: 5,778 K<br>Luminosity: 1.0 L☉<br><extra></extra>"),
    )
)

# Region annotations
region_labels = {
    "Main Sequence": dict(x=8000, y=0.5, ax=-80, ay=-40),
    "Red Giants": dict(x=3800, y=800, ax=-60, ay=-40),
    "Supergiants": dict(x=10000, y=200000, ax=60, ay=40),
    "White Dwarfs": dict(x=15000, y=0.0003, ax=60, ay=40),
}

for label, pos in region_labels.items():
    fig.add_annotation(
        x=np.log10(pos["x"]),
        y=np.log10(pos["y"]),
        xref="x",
        yref="y",
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=18, color="#555555"),
        bgcolor="rgba(255,255,255,0.7)",
        borderpad=4,
    )

# Style
fig.update_layout(
    title=dict(text="scatter-hr-diagram · plotly · pyplots.ai", font=dict(size=28), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="Surface Temperature (K)", font=dict(size=22)),
        tickfont=dict(size=18),
        type="log",
        autorange="reversed",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        showline=True,
        linecolor="#333333",
        linewidth=1,
        dtick=None,
        tickvals=[2500, 5000, 10000, 20000, 40000],
        ticktext=["2,500", "5,000", "10,000", "20,000", "40,000"],
    ),
    yaxis=dict(
        title=dict(text="Luminosity (L☉)", font=dict(size=22)),
        tickfont=dict(size=18),
        type="log",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        showline=True,
        linecolor="#333333",
        linewidth=1,
    ),
    template="plotly_white",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    legend=dict(
        title=dict(text="Spectral Type", font=dict(size=18)),
        font=dict(size=16),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(0,0,0,0.1)",
        borderwidth=1,
        x=0.01,
        y=0.01,
        xanchor="left",
        yanchor="bottom",
    ),
    width=1600,
    height=900,
    margin=dict(l=80, r=40, t=80, b=80),
)

# Secondary x-axis with spectral class labels
spectral_temps = {"O": 35000, "B": 20000, "A": 8750, "F": 6750, "G": 5600, "K": 4450, "M": 3050}

# Invisible trace to activate the secondary x-axis
fig.add_trace(
    go.Scatter(
        x=[35000], y=[1], xaxis="x2", mode="markers", marker=dict(size=0, opacity=0), showlegend=False, hoverinfo="skip"
    )
)

fig.update_layout(
    xaxis2=dict(
        tickfont=dict(size=18, color="#555555"),
        overlaying="x",
        side="top",
        type="log",
        range=[np.log10(45000), np.log10(2000)],
        tickvals=list(spectral_temps.values()),
        ticktext=list(spectral_temps.keys()),
        showgrid=False,
        showline=True,
        linecolor="#333333",
        linewidth=1,
        matches="x",
    ),
    margin=dict(l=80, r=40, t=100, b=80),
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
