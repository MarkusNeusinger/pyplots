""" pyplots.ai
campbell-basic: Campbell Diagram
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 79/100 | Created: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data
np.random.seed(42)
rpm = np.linspace(0, 6000, 80)

# Natural frequency modes (Hz) — slight variation with speed due to gyroscopic effects
mode_1_bending = 18 + 0.0008 * rpm + 0.4 * np.sin(rpm / 1500)
mode_2_bending = 42 - 0.0005 * rpm + 0.3 * np.cos(rpm / 2000)
mode_1_torsional = 55 + 0.0012 * rpm
mode_axial = 72 - 0.0003 * rpm + 0.5 * np.sin(rpm / 1200)
mode_3_bending = 90 + 0.0006 * rpm

modes = {
    "1st Bending": mode_1_bending,
    "2nd Bending": mode_2_bending,
    "1st Torsional": mode_1_torsional,
    "Axial": mode_axial,
    "3rd Bending": mode_3_bending,
}

# Engine order lines: frequency = order * rpm / 60
engine_orders = [1, 2, 3]
eo_frequencies = {order: order * rpm / 60 for order in engine_orders}

# Find critical speed intersections (engine order lines crossing natural frequency curves)
critical_speeds = []
critical_freqs = []
critical_labels = []

for mode_name, mode_freq in modes.items():
    for order in engine_orders:
        eo_freq = order * rpm / 60
        diff = mode_freq - eo_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            intersect_rpm = rpm[idx] + frac * (rpm[idx + 1] - rpm[idx])
            intersect_freq = order * intersect_rpm / 60
            if 200 < intersect_rpm < 5800:
                critical_speeds.append(intersect_rpm)
                critical_freqs.append(intersect_freq)
                critical_labels.append(f"{mode_name} / {order}x")

# Plot
sns.set_context("talk", font_scale=1.1)
fig, ax = plt.subplots(figsize=(16, 9))

# Natural frequency curves
mode_palette = ["#306998", "#E8822A", "#2CA02C", "#9467BD", "#17BECF"]
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    sns.lineplot(x=rpm, y=mode_freq, ax=ax, color=mode_palette[i], linewidth=2.8, label=mode_name)

# Engine order lines — label each along the line at a readable position
eo_color = "#999999"
eo_label_rpm = {1: 5200, 2: 2650, 3: 1700}
for order in engine_orders:
    ax.plot(rpm, eo_frequencies[order], color=eo_color, linewidth=1.8, linestyle="--", alpha=0.7)
    label_rpm = eo_label_rpm[order]
    label_freq = order * label_rpm / 60
    ax.text(
        label_rpm,
        label_freq + 2.5,
        f"{order}x",
        fontsize=15,
        color="#555555",
        fontweight="bold",
        va="bottom",
        ha="center",
        bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none", "alpha": 0.8},
    )

# Critical speed markers
ax.scatter(
    critical_speeds,
    critical_freqs,
    color="#D62728",
    s=180,
    zorder=5,
    edgecolors="white",
    linewidth=1.5,
    label="Critical Speeds",
)

# Style
ax.set_xlabel("Rotational Speed (RPM)", fontsize=20)
ax.set_ylabel("Frequency (Hz)", fontsize=20)
ax.set_title("campbell-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.15, linewidth=0.5)
ax.set_xlim(0, 6000)
ax.set_ylim(0, 110)

ax.legend(fontsize=14, loc="lower right", frameon=True, fancybox=False, edgecolor="#cccccc", framealpha=0.9, ncol=2)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
