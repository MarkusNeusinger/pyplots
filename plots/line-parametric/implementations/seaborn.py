"""pyplots.ai
line-parametric: Parametric Curve Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-20
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.collections import LineCollection


sns.set_theme(style="whitegrid")

# Data
t_lissajous = np.linspace(0, 2 * np.pi, 1000)
x_lissajous = np.sin(3 * t_lissajous)
y_lissajous = np.sin(2 * t_lissajous)

t_spiral = np.linspace(0, 4 * np.pi, 1000)
x_spiral = t_spiral * np.cos(t_spiral)
y_spiral = t_spiral * np.sin(t_spiral)

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

# Lissajous figure with color gradient
points_l = np.array([x_lissajous, y_lissajous]).T.reshape(-1, 1, 2)
segments_l = np.concatenate([points_l[:-1], points_l[1:]], axis=1)
norm_l = plt.Normalize(t_lissajous.min(), t_lissajous.max())
lc1 = LineCollection(segments_l, cmap="viridis", norm=norm_l, linewidth=3)
lc1.set_array(t_lissajous[:-1])
ax1.add_collection(lc1)
ax1.autoscale()

ax1.plot(x_lissajous[0], y_lissajous[0], "o", color="#306998", markersize=12, zorder=5, label="Start (t=0)")
ax1.plot(x_lissajous[-1], y_lissajous[-1], "s", color="#e74c3c", markersize=12, zorder=5, label="End (t=2π)")

# Spiral with color gradient
points_s = np.array([x_spiral, y_spiral]).T.reshape(-1, 1, 2)
segments_s = np.concatenate([points_s[:-1], points_s[1:]], axis=1)
norm_s = plt.Normalize(t_spiral.min(), t_spiral.max())
lc2 = LineCollection(segments_s, cmap="plasma", norm=norm_s, linewidth=3)
lc2.set_array(t_spiral[:-1])
ax2.add_collection(lc2)
ax2.autoscale()

ax2.plot(x_spiral[0], y_spiral[0], "o", color="#306998", markersize=12, zorder=5, label="Start (t=0)")
ax2.plot(x_spiral[-1], y_spiral[-1], "s", color="#e74c3c", markersize=12, zorder=5, label="End (t=4π)")

# Style
ax1.set_aspect("equal")
ax1.set_title("Lissajous: x=sin(3t), y=sin(2t)", fontsize=20, fontweight="medium")
ax1.set_xlabel("x(t)", fontsize=18)
ax1.set_ylabel("y(t)", fontsize=18)
ax1.tick_params(axis="both", labelsize=14)
ax1.legend(fontsize=14, loc="upper right")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(True, alpha=0.2, linewidth=0.8)
cb1 = fig.colorbar(lc1, ax=ax1, label="Parameter t", shrink=0.8)
cb1.ax.tick_params(labelsize=12)
cb1.set_label("Parameter t", fontsize=14)

ax2.set_aspect("equal")
ax2.set_title("Archimedean Spiral: x=t·cos(t), y=t·sin(t)", fontsize=20, fontweight="medium")
ax2.set_xlabel("x(t)", fontsize=18)
ax2.set_ylabel("y(t)", fontsize=18)
ax2.tick_params(axis="both", labelsize=14)
ax2.legend(fontsize=14, loc="upper right")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(True, alpha=0.2, linewidth=0.8)
cb2 = fig.colorbar(lc2, ax=ax2, label="Parameter t", shrink=0.8)
cb2.ax.tick_params(labelsize=12)
cb2.set_label("Parameter t", fontsize=14)

fig.suptitle("line-parametric · seaborn · pyplots.ai", fontsize=24, fontweight="medium", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
