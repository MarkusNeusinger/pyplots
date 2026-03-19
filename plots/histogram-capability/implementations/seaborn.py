""" pyplots.ai
histogram-capability: Process Capability Plot with Specification Limits
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-19
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# Data
np.random.seed(42)
measurements = np.random.normal(loc=10.00, scale=0.015, size=200)
lsl = 9.95
usl = 10.05
target = 10.00

mean = np.mean(measurements)
sigma = np.std(measurements, ddof=1)
cp = (usl - lsl) / (6 * sigma)
cpk = min((usl - mean) / (3 * sigma), (mean - lsl) / (3 * sigma))

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.histplot(
    measurements, bins=25, stat="density", color="#306998", edgecolor="white", linewidth=0.8, alpha=0.75, ax=ax
)

x_curve = np.linspace(mean - 4 * sigma, mean + 4 * sigma, 300)
y_curve = stats.norm.pdf(x_curve, mean, sigma)
ax.plot(x_curve, y_curve, color="#1a3a5c", linewidth=3, label="Fitted Normal")

ax.axvline(lsl, color="#c0392b", linestyle="--", linewidth=2.5, label=f"LSL = {lsl}")
ax.axvline(usl, color="#c0392b", linestyle="--", linewidth=2.5, label=f"USL = {usl}")
ax.axvline(target, color="#27ae60", linestyle="--", linewidth=2.5, label=f"Target = {target}")

# Capability indices annotation
annotation_text = f"Cp = {cp:.2f}\nCpk = {cpk:.2f}\n\u03bc = {mean:.4f}\n\u03c3 = {sigma:.4f}"
ax.text(
    0.97,
    0.95,
    annotation_text,
    transform=ax.transAxes,
    fontsize=18,
    verticalalignment="top",
    horizontalalignment="right",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.9},
)

# Style
ax.set_xlabel("Shaft Diameter (mm)", fontsize=20)
ax.set_ylabel("Density", fontsize=20)
ax.set_title("histogram-capability \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=16, frameon=False, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
