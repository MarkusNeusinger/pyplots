"""pyplots.ai
campbell-basic: Campbell Diagram
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) - slight variation with speed due to gyroscopic effects
mode_1_bending = 18 + 0.0008 * speed_rpm
mode_2_bending = 45 - 0.0005 * speed_rpm
mode_1_torsional = 62 + 0.0003 * speed_rpm
mode_axial = 78 - 0.0006 * speed_rpm
mode_3_bending = 95 + 0.0004 * speed_rpm

modes = [mode_1_bending, mode_2_bending, mode_1_torsional, mode_axial, mode_3_bending]
mode_labels = ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "3rd Bending"]
mode_colors = ["#306998", "#E8833A", "#4DAF4A", "#984EA3", "#A65628"]

# Engine order lines
engine_orders = [1, 2, 3]
eo_freq = {eo: eo * speed_hz for eo in engine_orders}

# Find critical speed intersections (where EO lines cross mode curves)
critical_speeds = []
critical_freqs = []
for mode in modes:
    for eo in engine_orders:
        eo_freqs = eo * speed_hz
        diff = mode - eo_freqs
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            rpm_interp = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            freq_interp = mode[idx] + frac * (mode[idx + 1] - mode[idx])
            if 100 < rpm_interp < 5900:
                critical_speeds.append(rpm_interp)
                critical_freqs.append(freq_interp)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
y_max = 110

for mode, label, color in zip(modes, mode_labels, mode_colors, strict=True):
    ax.plot(speed_rpm, mode, linewidth=3, color=color, label=label, zorder=3)

for eo in engine_orders:
    eo_line = eo_freq[eo]
    visible = eo_line <= y_max
    ax.plot(
        speed_rpm[visible],
        eo_line[visible],
        linewidth=2,
        color="#888888",
        linestyle="--",
        alpha=0.7,
        label=f"{eo}x EO",
        zorder=2,
    )

ax.scatter(
    critical_speeds,
    critical_freqs,
    s=250,
    color="#D62728",
    edgecolors="white",
    linewidth=1.5,
    zorder=5,
    label="Critical Speeds",
)

# Engine order line labels inside the plot area
for eo in engine_orders:
    eo_line = eo * speed_hz
    mask = eo_line <= y_max * 0.95
    if np.any(mask):
        last_idx = np.where(mask)[0][-1]
        label_rpm = speed_rpm[last_idx]
        label_freq = eo_line[last_idx]
        ax.text(
            label_rpm,
            label_freq + 2,
            f"{eo}x",
            fontsize=15,
            color="#666666",
            va="bottom",
            ha="center",
            fontweight="bold",
        )

# Style
ax.set_xlabel("Rotational Speed (RPM)", fontsize=20)
ax.set_ylabel("Frequency (Hz)", fontsize=20)
ax.set_title("campbell-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(0, 6000)
ax.set_ylim(0, y_max)
ax.legend(fontsize=14, loc="upper left", framealpha=0.9, edgecolor="none")
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
