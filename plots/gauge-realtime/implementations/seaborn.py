"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for better aesthetics
sns.set_theme(style="white")

# Data - Simulated CPU usage
np.random.seed(42)
current_value = 67  # Current CPU percentage
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green/Yellow/Red zones

# Previous values for motion blur effect (simulating real-time updates)
previous_values = [52, 58, 63, 67]  # Showing recent history of values

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Gauge parameters
center = (0.5, 0.15)
radius = 0.4
start_angle = 180  # Left side (0 degrees is right side)

# Zone colors (green/yellow/red)
zone_colors = ["#2ecc71", "#f1c40f", "#e74c3c"]  # Green, Yellow, Red

# Draw color zones as wedges
zone_starts = [min_value] + thresholds
zone_ends = thresholds + [max_value]

for i, (z_start, z_end) in enumerate(zip(zone_starts, zone_ends, strict=True)):
    # Convert value range to angle range
    angle_start = start_angle - (z_start / max_value) * 180
    angle_end = start_angle - (z_end / max_value) * 180

    wedge = mpatches.Wedge(
        center,
        radius,
        angle_end,
        angle_start,
        width=0.12,
        facecolor=zone_colors[i],
        edgecolor="white",
        linewidth=2,
        alpha=0.9,
    )
    ax.add_patch(wedge)

# Draw inner arc (dark background)
inner_wedge = mpatches.Wedge(center, radius - 0.12, 0, 180, facecolor="#2c3e50", edgecolor="none", alpha=0.3)
ax.add_patch(inner_wedge)

# Draw tick marks and labels
tick_values = [0, 25, 50, 75, 100]
for tick_val in tick_values:
    angle_rad = np.radians(start_angle - (tick_val / max_value) * 180)

    # Tick line
    inner_r = radius - 0.12
    outer_r = radius + 0.02
    x_inner = center[0] + inner_r * np.cos(angle_rad)
    y_inner = center[1] + inner_r * np.sin(angle_rad)
    x_outer = center[0] + outer_r * np.cos(angle_rad)
    y_outer = center[1] + outer_r * np.sin(angle_rad)
    ax.plot([x_inner, x_outer], [y_inner, y_outer], color="#2c3e50", linewidth=2)

    # Tick label
    label_r = radius + 0.06
    x_label = center[0] + label_r * np.cos(angle_rad)
    y_label = center[1] + label_r * np.sin(angle_rad)
    ax.text(x_label, y_label, str(tick_val), ha="center", va="center", fontsize=16, fontweight="bold", color="#2c3e50")

# Draw motion blur effect - previous needle positions with decreasing opacity
alphas = [0.1, 0.15, 0.2, 0.3]
for prev_val, alpha in zip(previous_values[:-1], alphas[:-1], strict=True):
    angle_rad = np.radians(start_angle - (prev_val / max_value) * 180)
    needle_length = radius - 0.15
    x_end = center[0] + needle_length * np.cos(angle_rad)
    y_end = center[1] + needle_length * np.sin(angle_rad)
    ax.plot([center[0], x_end], [center[1], y_end], color="#306998", linewidth=6, alpha=alpha, solid_capstyle="round")

# Draw main needle
angle_rad = np.radians(start_angle - (current_value / max_value) * 180)
needle_length = radius - 0.15
x_end = center[0] + needle_length * np.cos(angle_rad)
y_end = center[1] + needle_length * np.sin(angle_rad)
ax.plot([center[0], x_end], [center[1], y_end], color="#306998", linewidth=8, solid_capstyle="round", zorder=5)

# Draw needle center circle
center_circle = plt.Circle(center, 0.03, facecolor="#306998", edgecolor="white", linewidth=2, zorder=6)
ax.add_patch(center_circle)

# Display current value prominently
ax.text(
    center[0],
    center[1] - 0.08,
    f"{current_value}%",
    ha="center",
    va="top",
    fontsize=48,
    fontweight="bold",
    color="#306998",
)

# Label
ax.text(center[0], center[1] - 0.18, "CPU Usage", ha="center", va="top", fontsize=20, color="#7f8c8d")

# Min/Max labels
ax.text(
    center[0] - radius - 0.02, center[1] - 0.02, f"{min_value}%", ha="right", va="center", fontsize=14, color="#7f8c8d"
)
ax.text(
    center[0] + radius + 0.02, center[1] - 0.02, f"{max_value}%", ha="left", va="center", fontsize=14, color="#7f8c8d"
)

# Real-time indicator (pulsing dot)
pulse_circle = plt.Circle((center[0] + 0.35, center[1] + 0.35), 0.015, facecolor="#e74c3c", edgecolor="none", alpha=0.8)
ax.add_patch(pulse_circle)
ax.text(
    center[0] + 0.38, center[1] + 0.35, "LIVE", ha="left", va="center", fontsize=14, fontweight="bold", color="#e74c3c"
)

# Title
ax.set_title("gauge-realtime · seaborn · pyplots.ai", fontsize=24, fontweight="bold", color="#2c3e50", pad=20)

# Set equal aspect ratio and limits
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.15, 0.7)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
