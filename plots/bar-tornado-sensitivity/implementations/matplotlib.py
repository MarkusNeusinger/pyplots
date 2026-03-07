""" pyplots.ai
bar-tornado-sensitivity: Tornado Diagram for Sensitivity Analysis
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 87/100 | Created: 2026-03-07
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# Data — NPV sensitivity analysis for a capital investment project
base_npv = 12.5  # Base case NPV in $M

parameters = [
    "Discount Rate",
    "Revenue Growth",
    "Initial CapEx",
    "Operating Costs",
    "Tax Rate",
    "Terminal Value",
    "Working Capital",
    "Inflation Rate",
    "Project Duration",
    "Salvage Value",
]

low_npv = np.array([16.8, 8.2, 14.9, 15.1, 14.0, 10.1, 13.6, 13.4, 10.9, 11.8])
high_npv = np.array([9.1, 17.3, 10.4, 10.2, 11.2, 15.4, 11.5, 11.7, 14.3, 13.3])

# Sort by total range (widest bar at top)
total_range = np.abs(high_npv - low_npv)
sort_idx = np.argsort(total_range)
parameters = [parameters[i] for i in sort_idx]
low_npv = low_npv[sort_idx]
high_npv = high_npv[sort_idx]

# Compute bar segments relative to base
low_delta = low_npv - base_npv
high_delta = high_npv - base_npv

y_pos = np.arange(len(parameters))

# Colorblind-safe palette: teal + warm coral
color_low = "#2A9D8F"
color_high = "#E76F51"

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.barh(
    y_pos, low_delta, left=base_npv, height=0.6, color=color_low, label="Low Scenario", edgecolor="white", linewidth=0.5
)
ax.barh(
    y_pos,
    high_delta,
    left=base_npv,
    height=0.6,
    color=color_high,
    label="High Scenario",
    edgecolor="white",
    linewidth=0.5,
)

# Bar-end value labels
for i in range(len(parameters)):
    # Low scenario label
    lx = low_npv[i]
    offset = -0.15 if low_delta[i] < 0 else 0.15
    ha = "right" if low_delta[i] < 0 else "left"
    ax.text(lx + offset, y_pos[i], f"${lx:.1f}M", va="center", ha=ha, fontsize=11, fontweight="medium", color=color_low)

    # High scenario label
    hx = high_npv[i]
    offset = 0.15 if high_delta[i] > 0 else -0.15
    ha = "left" if high_delta[i] > 0 else "right"
    ax.text(
        hx + offset, y_pos[i], f"${hx:.1f}M", va="center", ha=ha, fontsize=11, fontweight="medium", color=color_high
    )

# Base case reference line with annotation
ax.axvline(x=base_npv, color="#444444", linewidth=1.5, linestyle="-", zorder=3)
ax.text(
    base_npv + 0.15,
    len(parameters) - 0.5,
    f"  Base Case: ${base_npv:.1f}M",
    fontsize=13,
    fontweight="bold",
    color="#444444",
    ha="left",
    va="center",
)

# X-axis dollar formatting using FuncFormatter
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

# Style
ax.set_yticks(y_pos)
ax.set_yticklabels(parameters, fontsize=16)
ax.set_xlabel("Net Present Value", fontsize=20)
ax.set_title("bar-tornado-sensitivity · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="x", labelsize=16)
ax.tick_params(axis="y", length=0)
ax.legend(fontsize=16, loc="lower right", frameon=False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.xaxis.grid(True, alpha=0.2, linewidth=0.8)

# Add padding to x-axis so labels don't clip
xlim = ax.get_xlim()
ax.set_xlim(xlim[0] - 0.8, xlim[1] + 0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
