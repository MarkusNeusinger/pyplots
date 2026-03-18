"""pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-03-18
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)

transit_center = 0.5
transit_duration = 0.08
transit_depth = 0.01
u1, u2 = 0.3, 0.1
half_dur = transit_duration / 2.0
n_points = 500

# Phase-folded observations
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Quadratic limb-darkened transit model for observations
model_flux = np.ones(n_points)
in_transit = np.abs(phase - transit_center) < half_dur
z = np.abs(phase[in_transit] - transit_center) / half_dur
limb = 1.0 - u1 * (1 - np.sqrt(1 - z**2)) - u2 * (1 - np.sqrt(1 - z**2)) ** 2
model_flux[in_transit] = 1.0 - transit_depth * limb

# Simulated photometry with realistic noise
flux_err = np.random.uniform(0.0008, 0.0020, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

# Smooth model curve for overlay
phase_smooth = np.linspace(0.0, 1.0, 2000)
model_smooth = np.ones(2000)
in_transit_s = np.abs(phase_smooth - transit_center) < half_dur
z_s = np.abs(phase_smooth[in_transit_s] - transit_center) / half_dur
limb_s = 1.0 - u1 * (1 - np.sqrt(1 - z_s**2)) - u2 * (1 - np.sqrt(1 - z_s**2)) ** 2
model_smooth[in_transit_s] = 1.0 - transit_depth * limb_s

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.errorbar(
    phase,
    flux,
    yerr=flux_err,
    fmt="o",
    markersize=5,
    color="#306998",
    ecolor="#306998",
    elinewidth=0.8,
    alpha=0.5,
    markeredgecolor="white",
    markeredgewidth=0.3,
    capsize=0,
    zorder=2,
    label="Photometry",
)

ax.plot(phase_smooth, model_smooth, color="#E74C3C", linewidth=3, zorder=3, label="Transit model")

# Style
ax.set_xlabel("Orbital Phase", fontsize=20)
ax.set_ylabel("Relative Flux", fontsize=20)
ax.set_title("lightcurve-transit \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.legend(fontsize=16, frameon=False)
ax.set_xlim(0.0, 1.0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
