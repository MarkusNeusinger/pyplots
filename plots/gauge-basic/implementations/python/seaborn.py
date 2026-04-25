"""anyplot.ai
gauge-basic: Basic Gauge Chart
Library: seaborn 0.13.2 | Python 3.13
Quality: pending | Updated: 2026-04-25
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Okabe-Ito zone colors (semantic gauge mapping: vermillion / orange / brand green)
ZONE_LOW = "#D55E00"
ZONE_MED = "#E69F00"
ZONE_HIGH = "#009E73"

# Data — sales performance gauge
value = 72
min_value = 0
max_value = 100
thresholds = [30, 70]

# Gauge geometry
center = (0.5, 0.32)
radius = 0.42
width = 0.18
start_angle = 180
end_angle = 0
angle_range = start_angle - end_angle
value_range = max_value - min_value

# Build dense scatter points across the arc, one row per (zone, value, radial offset)
n_points_per_zone = 60
zone_boundaries = [min_value] + thresholds + [max_value]
zone_names = ["Low", "Medium", "High"]
zone_colors = [ZONE_LOW, ZONE_MED, ZONE_HIGH]

zone_rows = []
for i in range(len(zone_boundaries) - 1):
    z_start = zone_boundaries[i]
    z_end = zone_boundaries[i + 1]
    for v in np.linspace(z_start, z_end, n_points_per_zone, endpoint=(i == len(zone_boundaries) - 2)):
        angle = start_angle - (v - min_value) / value_range * angle_range
        rad = np.radians(angle)
        for r_offset in np.linspace(-width / 2 + 0.01, width / 2 - 0.01, 8):
            r = radius + r_offset
            zone_rows.append(
                {"x": center[0] + r * np.cos(rad), "y": center[1] + r * np.sin(rad), "zone": zone_names[i]}
            )
df_zones = pd.DataFrame(zone_rows)

# Plot
sns.set_theme(
    style="white",
    rc={
        "figure.facecolor": PAGE_BG,
        "axes.facecolor": PAGE_BG,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
    },
)
fig, ax = plt.subplots(figsize=(16, 9), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)

# Arc — three coloured zones drawn with seaborn scatterplot
sns.scatterplot(
    data=df_zones,
    x="x",
    y="y",
    hue="zone",
    hue_order=zone_names,
    palette=zone_colors,
    s=200,
    marker="o",
    edgecolor="none",
    alpha=1.0,
    legend=False,
    ax=ax,
)

# Boundary cuts between zones — short radial line in the page background
for threshold in thresholds:
    boundary_angle = start_angle - (threshold - min_value) / value_range * angle_range
    rad = np.radians(boundary_angle)
    boundary_df = pd.DataFrame(
        {
            "x": [center[0] + r * np.cos(rad) for r in np.linspace(radius - width / 2, radius + width / 2, 12)],
            "y": [center[1] + r * np.sin(rad) for r in np.linspace(radius - width / 2, radius + width / 2, 12)],
        }
    )
    sns.lineplot(data=boundary_df, x="x", y="y", color=PAGE_BG, linewidth=4, ax=ax, legend=False)

# Needle
needle_angle = start_angle - (value - min_value) / value_range * angle_range
needle_rad = np.radians(needle_angle)
needle_length = radius + width / 2 - 0.015
needle_tip_x = center[0] + needle_length * np.cos(needle_rad)
needle_tip_y = center[1] + needle_length * np.sin(needle_rad)

needle_df = pd.DataFrame({"x": [center[0], needle_tip_x], "y": [center[1], needle_tip_y]})
sns.lineplot(data=needle_df, x="x", y="y", color=INK, linewidth=6, ax=ax, legend=False)

# Hub — outer ring (page bg) + inner disc (ink) for clean contrast in both themes
hub_df = pd.DataFrame({"x": [center[0]], "y": [center[1]]})
sns.scatterplot(data=hub_df, x="x", y="y", s=1400, color=PAGE_BG, edgecolor="none", ax=ax, legend=False, zorder=10)
sns.scatterplot(data=hub_df, x="x", y="y", s=900, color=INK, edgecolor="none", ax=ax, legend=False, zorder=11)

# Value display
ax.text(center[0], center[1] - 0.20, f"{value}%", ha="center", va="center", fontsize=56, fontweight="bold", color=INK)

# Min / max endpoint labels
for vlabel, x_off in [(min_value, -1), (max_value, 1)]:
    ax.text(
        center[0] + x_off * radius, center[1] - 0.06, f"{vlabel}", ha="center", va="top", fontsize=20, color=INK_SOFT
    )

# Zone labels on the arc — white text with dark outline reads on every zone in both themes
zone_label_centers = [
    (thresholds[0] - min_value) / 2 + min_value,
    (thresholds[0] + thresholds[1]) / 2,
    (thresholds[1] + max_value) / 2,
]
for v_center, label in zip(zone_label_centers, zone_names, strict=True):
    angle = start_angle - (v_center - min_value) / value_range * angle_range
    rad = np.radians(angle)
    lx = center[0] + radius * np.cos(rad)
    ly = center[1] + radius * np.sin(rad)
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        ax.text(
            lx + dx * 0.0035,
            ly + dy * 0.0035,
            label,
            ha="center",
            va="center",
            fontsize=22,
            color="#1a1a1a",
            fontweight="bold",
        )
    ax.text(lx, ly, label, ha="center", va="center", fontsize=22, color="white", fontweight="bold")

# Title and subtitle
ax.set_title(
    "Sales Performance · gauge-basic · seaborn · anyplot.ai", fontsize=24, fontweight="medium", pad=20, color=INK
)

# Axis settings — purely a canvas
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
