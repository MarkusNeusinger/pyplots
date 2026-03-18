"""pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-18
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)

n_points = 500
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Transit parameters
transit_center = 0.5
transit_width = 0.025
transit_depth = 0.01
u1, u2 = 0.4, 0.2

# Transit model for data points
z = np.abs(phase - transit_center) / transit_width
dip = np.where(z < 1.0, np.sqrt(np.clip(1.0 - z**2, 0, None)), 0.0)
limb = 1.0 - u1 * (1 - dip) - u2 * (1 - dip) ** 2
model_flux = 1.0 - transit_depth * dip * limb

# Observed flux with noise
flux_err = np.random.uniform(0.0008, 0.0015, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

# Smooth model curve for overlay
phase_model = np.linspace(0.0, 1.0, 2000)
z_model = np.abs(phase_model - transit_center) / transit_width
dip_model = np.where(z_model < 1.0, np.sqrt(np.clip(1.0 - z_model**2, 0, None)), 0.0)
limb_model = 1.0 - u1 * (1 - dip_model) - u2 * (1 - dip_model) ** 2
model_smooth = 1.0 - transit_depth * dip_model * limb_model

df = pd.DataFrame({"phase": phase, "flux": flux, "flux_err": flux_err})

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.errorbar(
    df["phase"],
    df["flux"],
    yerr=df["flux_err"],
    fmt="none",
    ecolor="#306998",
    elinewidth=0.8,
    alpha=0.35,
    capsize=0,
    zorder=1,
)

sns.scatterplot(
    data=df, x="phase", y="flux", color="#306998", s=50, alpha=0.6, edgecolor="white", linewidth=0.4, ax=ax, zorder=2
)

ax.plot(phase_model, model_smooth, color="#E34234", linewidth=2.5, zorder=3, label="Transit model")

# Style
ax.set_xlabel("Orbital Phase", fontsize=20)
ax.set_ylabel("Relative Flux", fontsize=20)
ax.set_title("lightcurve-transit · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.legend(fontsize=16, frameon=False, loc="lower right")

ax.set_xlim(0.0, 1.0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
