""" pyplots.ai
campbell-basic: Campbell Diagram
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 87/100 | Created: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


# Data
speed_rpm = np.linspace(0, 6000, 200)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) - pronounced gyroscopic effects
# Forward whirl modes increase with speed, backward whirl modes decrease
mode_1_bending = 18 + 0.004 * speed_rpm - 1.5e-7 * speed_rpm**2
mode_2_bending = 48 - 0.003 * speed_rpm + 2.0e-7 * speed_rpm**2
mode_1_torsional = 62 + 0.0004 * speed_rpm
mode_axial = 74 - 0.005 * speed_rpm + 4.0e-7 * speed_rpm**2
mode_3_bending = 88 + 0.005 * speed_rpm - 3.5e-7 * speed_rpm**2

modes = [mode_1_bending, mode_2_bending, mode_1_torsional, mode_axial, mode_3_bending]
mode_labels = ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "3rd Bending"]
mode_colors = ["#306998", "#E8833A", "#4DAF4A", "#984EA3", "#A65628"]

# Engine order lines
engine_orders = [1, 2, 3]
eo_freq = {eo: eo * speed_hz for eo in engine_orders}

# Find critical speed intersections
critical_speeds = []
critical_freqs = []
critical_labels = []
for mode, mlabel in zip(modes, mode_labels, strict=True):
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
                critical_labels.append(f"{mlabel}\n{eo}x @ {int(rpm_interp)} RPM")

# Define operating range for storytelling
op_min, op_max = 2500, 4500

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
y_max = 110

# Operating range shading
ax.axvspan(op_min, op_max, alpha=0.06, color="#306998", zorder=0)
ax.axvline(op_min, color="#306998", linewidth=1, linestyle=":", alpha=0.4, zorder=1)
ax.axvline(op_max, color="#306998", linewidth=1, linestyle=":", alpha=0.4, zorder=1)
ax.text(
    (op_min + op_max) / 2,
    3,
    "Operating Range",
    fontsize=13,
    color="#306998",
    ha="center",
    va="bottom",
    fontstyle="italic",
    alpha=0.6,
)

# Mode curves with varying linewidth for visual hierarchy
for mode, label, color in zip(modes, mode_labels, mode_colors, strict=True):
    ax.plot(speed_rpm, mode, linewidth=2.8, color=color, label=label, zorder=3, solid_capstyle="round")

# Engine order lines
for eo in engine_orders:
    eo_line = eo_freq[eo]
    visible = eo_line <= y_max
    ax.plot(
        speed_rpm[visible], eo_line[visible], linewidth=1.8, color="#AAAAAA", linestyle=(0, (8, 4)), alpha=0.6, zorder=2
    )

# Engine order labels placed along the lines using ax.annotate with rotation
for eo in engine_orders:
    eo_line = eo * speed_hz
    # Place label at ~30% along the visible line for clean positioning
    target_freq = y_max * 0.30
    target_rpm = target_freq * 60 / eo
    if target_rpm < 5800:
        angle_rad = np.arctan2(
            (eo * (speed_rpm[1] - speed_rpm[0]) / 60) * (9 / y_max), (speed_rpm[1] - speed_rpm[0]) * (16 / 6000)
        )
        angle_deg = np.degrees(angle_rad)
        ax.annotate(
            f"{eo}×",
            xy=(target_rpm, target_freq),
            fontsize=14,
            color="#777777",
            fontweight="bold",
            ha="center",
            va="bottom",
            rotation=angle_deg,
            rotation_mode="anchor",
            zorder=4,
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.8},
        )

# Critical speed markers - differentiate those in operating range
in_op = [(op_min <= s <= op_max) for s in critical_speeds]
out_op = [not x for x in in_op]

cs_arr = np.array(critical_speeds)
cf_arr = np.array(critical_freqs)
in_op_arr = np.array(in_op)
out_op_arr = np.array(out_op)

# Markers outside operating range (subtle)
if np.any(out_op_arr):
    ax.scatter(
        cs_arr[out_op_arr],
        cf_arr[out_op_arr],
        s=200,
        color="#D62728",
        edgecolors="white",
        linewidth=1.5,
        zorder=5,
        alpha=0.5,
    )

# Markers inside operating range (emphasized - the dangerous ones)
if np.any(in_op_arr):
    ax.scatter(
        cs_arr[in_op_arr],
        cf_arr[in_op_arr],
        s=350,
        color="#D62728",
        edgecolors="white",
        linewidth=2,
        zorder=6,
        marker="D",
    )
    # Annotate the most critical intersections (inside operating range)
    cl_arr = np.array(critical_labels)
    op_speeds = cs_arr[in_op_arr]
    op_freqs = cf_arr[in_op_arr]
    op_labels = cl_arr[in_op_arr]
    # Sort by frequency for alternating offset directions
    sort_idx = np.argsort(op_freqs)
    for i, si in enumerate(sort_idx):
        short_label = op_labels[si].split("\n")[0]
        # Alternate annotation direction to avoid overlaps
        if op_freqs[si] > y_max * 0.7:
            dx, dy = 20, -22  # point down for high-frequency intersections
        elif i % 2 == 0:
            dx, dy = 22, 16
        else:
            dx, dy = -22, -18
        ax.annotate(
            short_label,
            xy=(op_speeds[si], op_freqs[si]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=11,
            color="#B71C1C",
            fontweight="bold",
            arrowprops={"arrowstyle": "-", "color": "#B71C1C", "lw": 0.8},
            zorder=7,
            bbox={
                "boxstyle": "round,pad=0.2",
                "facecolor": "white",
                "edgecolor": "#B71C1C",
                "alpha": 0.85,
                "linewidth": 0.6,
            },
        )

# Style
ax.set_xlabel("Rotational Speed (RPM)", fontsize=20)
ax.set_ylabel("Frequency (Hz)", fontsize=20)
ax.set_title("campbell-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.6)
ax.spines["bottom"].set_linewidth(0.6)
ax.spines["left"].set_color("#555555")
ax.spines["bottom"].set_color("#555555")
ax.set_xlim(0, 6000)
ax.set_ylim(0, y_max)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.6, color="#CCCCCC")
ax.xaxis.grid(True, alpha=0.08, linewidth=0.4, color="#CCCCCC")

# Compact legend outside the plot area using matplotlib's bbox_to_anchor
legend_handles = ax.get_legend_handles_labels()
mode_handles = legend_handles[0][:5]
mode_names = legend_handles[1][:5]

# Add custom entries for EO lines and critical speeds
eo_handle = Line2D([0], [0], color="#AAAAAA", linewidth=1.8, linestyle=(0, (8, 4)), alpha=0.6)
crit_outside = Line2D(
    [0], [0], marker="o", color="none", markerfacecolor="#D62728", markeredgecolor="white", markersize=10, alpha=0.5
)
crit_inside = Line2D(
    [0], [0], marker="D", color="none", markerfacecolor="#D62728", markeredgecolor="white", markersize=10
)
op_handle = Patch(facecolor="#306998", alpha=0.12, edgecolor="none")

all_handles = mode_handles + [eo_handle, crit_outside, crit_inside, op_handle]
all_labels = mode_names + ["Engine Order (1×–3×)", "Critical Speed", "Critical (in op. range)", "Operating Range"]

ax.legend(
    all_handles,
    all_labels,
    fontsize=13,
    loc="upper left",
    bbox_to_anchor=(1.01, 1),
    framealpha=0.95,
    edgecolor="#DDDDDD",
    borderpad=0.8,
    labelspacing=0.7,
    handlelength=1.8,
)

fig.subplots_adjust(right=0.78)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
