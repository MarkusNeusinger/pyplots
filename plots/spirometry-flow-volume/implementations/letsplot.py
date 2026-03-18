""" pyplots.ai
spirometry-flow-volume: Spirometry Flow-Volume Loop
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 83/100 | Created: 2026-03-18
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data: Simulated spirometry flow-volume loop
np.random.seed(42)

# Measured patient data (mild obstructive pattern)
fvc = 4.2  # Forced Vital Capacity in liters
pef = 8.5  # Peak Expiratory Flow in L/s
fev1 = 3.1  # FEV1 in liters

# Expiratory limb: sharp rise to PEF then roughly linear decline
n_exp = 150
volume_exp = np.linspace(0, fvc, n_exp)
t_peak = 0.08  # PEF occurs early (~8% of FVC)
peak_idx = int(t_peak * n_exp)

# Rising phase to PEF
flow_rise = np.linspace(0, pef, peak_idx + 1)
# Declining phase after PEF (roughly linear with slight concavity for mild obstruction)
volume_remaining = volume_exp[peak_idx:]
flow_decline = pef * (1 - ((volume_remaining - volume_remaining[0]) / (fvc - volume_remaining[0])) ** 0.85)
flow_exp = np.concatenate([flow_rise, flow_decline[1:]])

# Inspiratory limb: symmetric U-shaped curve below zero
n_insp = 150
volume_insp = np.linspace(fvc, 0, n_insp)
pif = -6.0  # Peak Inspiratory Flow
t_norm = np.linspace(0, np.pi, n_insp)
flow_insp = pif * np.sin(t_norm)

# Predicted normal values (healthy reference)
fvc_pred = 4.8
pef_pred = 10.2

n_pred_exp = 150
volume_pred_exp = np.linspace(0, fvc_pred, n_pred_exp)
peak_idx_pred = int(0.08 * n_pred_exp)
flow_pred_rise = np.linspace(0, pef_pred, peak_idx_pred + 1)
volume_pred_remaining = volume_pred_exp[peak_idx_pred:]
flow_pred_decline = pef_pred * (
    1 - ((volume_pred_remaining - volume_pred_remaining[0]) / (fvc_pred - volume_pred_remaining[0])) ** 0.95
)
flow_pred_exp = np.concatenate([flow_pred_rise, flow_pred_decline[1:]])

n_pred_insp = 150
volume_pred_insp = np.linspace(fvc_pred, 0, n_pred_insp)
pif_pred = -7.0
flow_pred_insp = pif_pred * np.sin(np.linspace(0, np.pi, n_pred_insp))

# Combine into DataFrames
df_measured_exp = pd.DataFrame({"volume": volume_exp, "flow": flow_exp})
df_measured_insp = pd.DataFrame({"volume": volume_insp, "flow": flow_insp})
df_pred_exp = pd.DataFrame({"volume": volume_pred_exp, "flow": flow_pred_exp})
df_pred_insp = pd.DataFrame({"volume": volume_pred_insp, "flow": flow_pred_insp})

# PEF annotation point
pef_volume = volume_exp[np.argmax(flow_exp)]
df_pef = pd.DataFrame({"volume": [pef_volume], "flow": [pef]})

# Clinical values annotation
clinical_text = f"FEV1: {fev1:.1f} L\nFVC: {fvc:.1f} L\nPEF: {pef:.1f} L/s"
df_clinical = pd.DataFrame({"volume": [fvc * 0.75], "flow": [pef * 0.75], "label": [clinical_text]})

# Plot
plot = (
    ggplot()
    # Predicted loop (dashed, background)
    + geom_line(aes(x="volume", y="flow"), data=df_pred_exp, color="#B0B0B0", size=1.5, linetype="dashed")
    + geom_line(aes(x="volume", y="flow"), data=df_pred_insp, color="#B0B0B0", size=1.5, linetype="dashed")
    # Measured loop (solid, foreground)
    + geom_line(aes(x="volume", y="flow"), data=df_measured_exp, color="#306998", size=2.5)
    + geom_line(aes(x="volume", y="flow"), data=df_measured_insp, color="#306998", size=2.5)
    # PEF marker
    + geom_point(aes(x="volume", y="flow"), data=df_pef, color="#dc2626", size=8, shape=16)
    + geom_label(
        aes(x="volume", y="flow", label="label"),
        data=pd.DataFrame({"volume": [pef_volume + 0.25], "flow": [pef + 0.3], "label": [f"PEF: {pef} L/s"]}),
        size=13,
        color="#dc2626",
        fill="white",
        label_padding=0.3,
        hjust=0,
    )
    # Clinical values text box
    + geom_label(
        aes(x="volume", y="flow", label="label"),
        data=df_clinical,
        size=12,
        color="#333333",
        fill="#f8f8f8",
        label_padding=0.5,
        hjust=0,
    )
    # Zero flow reference line
    + geom_hline(yintercept=0, color="#999999", size=0.8)
    # Labels
    + labs(x="Volume (L)", y="Flow (L/s)", title="spirometry-flow-volume · letsplot · pyplots.ai")
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#e5e5e5", size=0.5),
        panel_grid_minor=element_blank(),
    )
)

# Save
ggsave(plot, "plot.png", scale=3, path=".")
ggsave(plot, "plot.html", path=".")
