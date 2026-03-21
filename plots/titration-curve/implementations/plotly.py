""" pyplots.ai
titration-curve: Acid-Base Titration Curve
Library: plotly 6.6.0 | Python 3.14.3
Quality: 87/100 | Created: 2026-03-21
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data — 25 mL of 0.1 M HCl titrated with 0.1 M NaOH
c_acid = 0.1
v_acid = 25.0
c_base = 0.1
volume_ml = np.concatenate([np.linspace(0.0, 24.0, 80), np.linspace(24.0, 26.0, 30), np.linspace(26.0, 50.0, 50)])
volume_ml = np.unique(volume_ml)

ph = np.zeros_like(volume_ml)
for i, v in enumerate(volume_ml):
    total_vol = (v_acid + v) / 1000.0
    moles_acid = c_acid * v_acid / 1000.0
    moles_base = c_base * v / 1000.0
    diff = moles_acid - moles_base

    if diff > 1e-10:
        h_conc = diff / total_vol
        ph[i] = -np.log10(h_conc)
    elif diff < -1e-10:
        oh_conc = -diff / total_vol
        poh = -np.log10(oh_conc)
        ph[i] = 14.0 - poh
    else:
        ph[i] = 7.0

ph = np.clip(ph, 0, 14)

# Derivative (dpH/dV) using central differences
dph_dv = np.gradient(ph, volume_ml)

# Equivalence point — theoretical value for strong acid/strong base
eq_volume = 25.0
eq_ph = 7.0

# Plot — dual y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=volume_ml, y=ph, mode="lines", name="pH", line=dict(color="#306998", width=3.5)), secondary_y=False
)

fig.add_trace(
    go.Scatter(x=volume_ml, y=dph_dv, mode="lines", name="dpH/dV", line=dict(color="#E8873A", width=2.5, dash="dot")),
    secondary_y=True,
)

# Equivalence point marker and vertical line
fig.add_vline(
    x=eq_volume,
    line_dash="dash",
    line_color="#888888",
    line_width=2,
    annotation_text=f"Equivalence Point<br>{eq_volume:.1f} mL, pH {eq_ph:.1f}",
    annotation_position="top left",
    annotation_font_size=16,
    annotation_font_color="#444444",
)

fig.add_trace(
    go.Scatter(
        x=[eq_volume],
        y=[eq_ph],
        mode="markers",
        name="Equivalence Point",
        marker=dict(size=14, color="#D64545", symbol="diamond", line=dict(width=2, color="white")),
        showlegend=False,
    ),
    secondary_y=False,
)

# Style
fig.update_layout(
    title=dict(text="HCl + NaOH Titration · titration-curve · plotly · pyplots.ai", font=dict(size=28)),
    template="plotly_white",
    legend=dict(font=dict(size=18), x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
    margin=dict(l=80, r=80, t=100, b=80),
)

fig.update_xaxes(
    title=dict(text="Volume of NaOH added (mL)", font=dict(size=22)),
    tickfont=dict(size=18),
    showgrid=False,
    showline=True,
    linewidth=1,
    linecolor="#CCCCCC",
)

fig.update_yaxes(
    title=dict(text="pH", font=dict(size=22)),
    tickfont=dict(size=18),
    range=[0, 14],
    showgrid=True,
    gridwidth=1,
    gridcolor="rgba(0,0,0,0.08)",
    showline=True,
    linewidth=1,
    linecolor="#CCCCCC",
    secondary_y=False,
)

fig.update_yaxes(
    title=dict(text="dpH/dV (mL⁻¹)", font=dict(size=22)),
    tickfont=dict(size=18),
    showgrid=False,
    showline=True,
    linewidth=1,
    linecolor="#CCCCCC",
    secondary_y=True,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
