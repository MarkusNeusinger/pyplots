""" pyplots.ai
spirometry-flow-volume: Spirometry Flow-Volume Loop
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-18
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulate realistic spirometry flow-volume loop
np.random.seed(42)

# Measured values (typical adult male, mild obstruction pattern)
fvc = 4.2  # Forced Vital Capacity (L)
pef = 8.5  # Peak Expiratory Flow (L/s)
fev1 = 3.1  # FEV1 (L)

# Predicted normal values
fvc_pred = 4.8
pef_pred = 10.2
fev1_pred = 4.0

# Expiratory limb - sharp rise to PEF then roughly linear decline
n_points = 200
volume_exp = np.linspace(0, fvc, n_points)
t_exp = volume_exp / fvc
# Two-phase model: rapid rise then linear-ish descent
rise = 1 - np.exp(-30 * t_exp)
decay = (1 - t_exp) ** 0.5
flow_exp_raw = rise * decay
flow_exp = flow_exp_raw / flow_exp_raw.max() * pef

# Inspiratory limb - measured (symmetric U-shape, negative flow)
volume_insp = np.linspace(fvc, 0, n_points)
t_insp = (fvc - volume_insp) / fvc
peak_insp_flow = 5.5
flow_insp = -peak_insp_flow * np.sin(np.pi * t_insp) ** 0.8

# Predicted expiratory limb
volume_exp_pred = np.linspace(0, fvc_pred, n_points)
t_exp_pred = volume_exp_pred / fvc_pred
rise_pred = 1 - np.exp(-30 * t_exp_pred)
decay_pred = (1 - t_exp_pred) ** 0.5
flow_exp_pred_raw = rise_pred * decay_pred
flow_exp_pred = flow_exp_pred_raw / flow_exp_pred_raw.max() * pef_pred

# Predicted inspiratory limb
volume_insp_pred = np.linspace(fvc_pred, 0, n_points)
t_insp_pred = (fvc_pred - volume_insp_pred) / fvc_pred
peak_insp_pred = 6.5
flow_insp_pred = -peak_insp_pred * np.sin(np.pi * t_insp_pred) ** 0.8

# Combine into full loops
volume_measured = np.concatenate([volume_exp, volume_insp])
flow_measured = np.concatenate([flow_exp, flow_insp])
volume_predicted = np.concatenate([volume_exp_pred, volume_insp_pred])
flow_predicted = np.concatenate([flow_exp_pred, flow_insp_pred])

# Find PEF point on measured curve
pef_idx = np.argmax(flow_exp)
pef_volume = volume_exp[pef_idx]
pef_flow = flow_exp[pef_idx]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(
    volume_predicted, flow_predicted, color="#999999", linewidth=2.5, linestyle="--", label="Predicted Normal", zorder=2
)
ax.plot(
    volume_measured, flow_measured, color="#306998", linewidth=3.5, solid_capstyle="round", label="Measured", zorder=3
)

# Mark PEF
ax.scatter(pef_volume, pef_flow, s=250, color="#306998", edgecolors="white", linewidth=1.5, zorder=4)
ax.annotate(
    f"PEF = {pef_flow:.1f} L/s",
    xy=(pef_volume, pef_flow),
    xytext=(pef_volume + 0.6, pef_flow - 0.6),
    fontsize=16,
    fontweight="bold",
    color="#306998",
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2, "connectionstyle": "arc3,rad=0.2"},
)

# Clinical values text box
textstr = (
    f"FVC = {fvc:.1f} L  (pred {fvc_pred:.1f})\n"
    f"FEV\u2081 = {fev1:.1f} L  (pred {fev1_pred:.1f})\n"
    f"FEV\u2081/FVC = {fev1 / fvc:.0%}\n"
    f"PEF = {pef_flow:.1f} L/s  (pred {pef_pred:.1f})"
)
props = {"boxstyle": "round,pad=0.6", "facecolor": "#f0f4f8", "edgecolor": "#306998", "alpha": 0.9, "linewidth": 1.5}
ax.text(
    0.97,
    0.97,
    textstr,
    transform=ax.transAxes,
    fontsize=15,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=props,
    family="monospace",
)

# Zero flow reference line
ax.axhline(y=0, color="#cccccc", linewidth=1, zorder=1)

# Style
ax.set_xlabel("Volume (L)", fontsize=20)
ax.set_ylabel("Flow (L/s)", fontsize=20)
ax.set_title("spirometry-flow-volume · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=16, loc="lower left", framealpha=0.9)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
