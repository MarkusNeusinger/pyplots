""" pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-19
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# Data - simulating CPU usage with realistic transitions
np.random.seed(42)
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green/Yellow/Red zones
current_value = 72  # Current CPU usage

# Previous values to show motion trail (simulating real-time updates)
previous_values = [65, 68, 70]  # Trail of recent positions

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect("equal")

# Gauge parameters
center = (0, 0)
outer_radius = 0.9
inner_radius = 0.6
arc_start = 135  # degrees (lower left)
arc_end = 45  # degrees (lower right, going through top)

# Color scheme for zones
zone_colors = ["#2ECC71", "#F1C40F", "#E74C3C"]  # Green, Yellow, Red

# Draw color zones
zone_boundaries = [min_value] + thresholds + [max_value]
for i in range(len(zone_boundaries) - 1):
    start_frac = (zone_boundaries[i] - min_value) / (max_value - min_value)
    end_frac = (zone_boundaries[i + 1] - min_value) / (max_value - min_value)

    # Convert to angles (arc goes from 135° counterclockwise to 45°, so total 270°)
    angle_start = arc_start - start_frac * 270
    angle_end = arc_start - end_frac * 270

    # Draw arc wedge
    wedge = mpatches.Wedge(
        center,
        outer_radius,
        angle_end,
        angle_start,
        width=outer_radius - inner_radius,
        facecolor=zone_colors[i],
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(wedge)

# Draw inner circle (gauge face)
inner_circle = plt.Circle(center, inner_radius - 0.05, color="#2C3E50", zorder=2)
ax.add_patch(inner_circle)

# Draw tick marks and labels
tick_values = np.linspace(min_value, max_value, 11)  # 0, 10, 20, ... 100
for i, val in enumerate(tick_values):
    frac = (val - min_value) / (max_value - min_value)
    angle_deg = arc_start - frac * 270
    angle_rad = np.radians(angle_deg)

    # Tick marks
    tick_inner = inner_radius - 0.02
    tick_outer = inner_radius + 0.05
    x_inner = tick_inner * np.cos(angle_rad)
    y_inner = tick_inner * np.sin(angle_rad)
    x_outer = tick_outer * np.cos(angle_rad)
    y_outer = tick_outer * np.sin(angle_rad)

    ax.plot([x_inner, x_outer], [y_inner, y_outer], color="white", linewidth=2, zorder=3)

    # Labels for major ticks (every 20)
    if i % 2 == 0:
        label_radius = inner_radius - 0.12
        x_label = label_radius * np.cos(angle_rad)
        y_label = label_radius * np.sin(angle_rad)
        ax.text(
            x_label,
            y_label,
            f"{int(val)}",
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
            color="white",
            zorder=4,
        )

# Draw motion trail (ghost needles showing previous positions)
for i, prev_val in enumerate(previous_values):
    alpha = 0.15 + i * 0.1  # Increasing opacity for more recent positions
    frac = (prev_val - min_value) / (max_value - min_value)
    angle_deg = arc_start - frac * 270
    angle_rad = np.radians(angle_deg)

    needle_length = inner_radius - 0.15
    x_needle = needle_length * np.cos(angle_rad)
    y_needle = needle_length * np.sin(angle_rad)

    ax.plot([0, x_needle], [0, y_needle], color="#ECF0F1", linewidth=6, alpha=alpha, zorder=5, solid_capstyle="round")

# Draw current needle
frac = (current_value - min_value) / (max_value - min_value)
angle_deg = arc_start - frac * 270
angle_rad = np.radians(angle_deg)

needle_length = inner_radius - 0.15
x_needle = needle_length * np.cos(angle_rad)
y_needle = needle_length * np.sin(angle_rad)

# Needle with motion blur effect
ax.plot([0, x_needle], [0, y_needle], color="#E74C3C", linewidth=10, zorder=6, solid_capstyle="round")
ax.plot([0, x_needle], [0, y_needle], color="#FFFFFF", linewidth=4, zorder=7, solid_capstyle="round")

# Center hub
hub = plt.Circle(center, 0.08, color="#E74C3C", zorder=8)
ax.add_patch(hub)
hub_inner = plt.Circle(center, 0.05, color="#FFFFFF", zorder=9)
ax.add_patch(hub_inner)

# Display current value prominently
ax.text(
    0, -0.15, f"{current_value}%", ha="center", va="center", fontsize=48, fontweight="bold", color="#FFFFFF", zorder=10
)
ax.text(0, -0.32, "CPU Usage", ha="center", va="center", fontsize=20, color="#BDC3C7", zorder=10)

# Add "LIVE" indicator to show real-time nature
live_box = mpatches.FancyBboxPatch(
    (-0.18, 0.15),
    0.36,
    0.15,
    boxstyle="round,pad=0.02,rounding_size=0.02",
    facecolor="#E74C3C",
    edgecolor="none",
    zorder=10,
)
ax.add_patch(live_box)
ax.text(0, 0.225, "● LIVE", ha="center", va="center", fontsize=16, fontweight="bold", color="white", zorder=11)

# Set limits and remove axes
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.axis("off")
ax.set_facecolor("#1A252F")
fig.patch.set_facecolor("#1A252F")

# Title
ax.set_title("gauge-realtime · matplotlib · pyplots.ai", fontsize=24, color="white", fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="#1A252F")
