""" pyplots.ai
gauge-basic: Basic Gauge Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-14
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")

# Data
value = 72
min_value = 0
max_value = 100
thresholds = [30, 70]  # Creates three zones: 0-30, 30-70, 70-100

# Colors for zones (red/yellow/green convention)
zone_colors = ["#E74C3C", "#F1C40F", "#27AE60"]  # red, yellow, green

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Gauge parameters
center = (0.5, 0.3)
radius = 0.35
start_angle = 180  # Left side
end_angle = 0  # Right side

# Draw colored arc segments for zones
zone_boundaries = [min_value] + thresholds + [max_value]
for i in range(len(zone_boundaries) - 1):
    # Convert value range to angle range (180 to 0 degrees)
    angle_start = 180 - (zone_boundaries[i] - min_value) / (max_value - min_value) * 180
    angle_end = 180 - (zone_boundaries[i + 1] - min_value) / (max_value - min_value) * 180

    # Create wedge for this zone
    wedge = patches.Wedge(
        center, radius, angle_end, angle_start, width=0.12, facecolor=zone_colors[i], edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)

# Draw inner arc (gray background for depth)
inner_wedge = patches.Wedge(center, radius - 0.12, 0, 180, width=0.02, facecolor="#BDC3C7", edgecolor="none")
ax.add_patch(inner_wedge)

# Calculate needle angle for current value
needle_angle = 180 - (value - min_value) / (max_value - min_value) * 180
needle_angle_rad = np.radians(needle_angle)

# Draw needle
needle_length = radius - 0.05
needle_x = center[0] + needle_length * np.cos(needle_angle_rad)
needle_y = center[1] + needle_length * np.sin(needle_angle_rad)

ax.annotate(
    "",
    xy=(needle_x, needle_y),
    xytext=center,
    arrowprops={"arrowstyle": "-|>", "color": "#2C3E50", "lw": 4, "mutation_scale": 20},
)

# Draw center circle (needle hub)
hub = plt.Circle(center, 0.04, color="#2C3E50", zorder=5)
ax.add_patch(hub)

# Add tick marks and labels
tick_values = [0, 25, 50, 75, 100]
for tick_val in tick_values:
    tick_angle = 180 - (tick_val - min_value) / (max_value - min_value) * 180
    tick_angle_rad = np.radians(tick_angle)

    # Tick mark positions
    inner_tick_r = radius + 0.02
    outer_tick_r = radius + 0.06
    label_r = radius + 0.12

    x_inner = center[0] + inner_tick_r * np.cos(tick_angle_rad)
    y_inner = center[1] + inner_tick_r * np.sin(tick_angle_rad)
    x_outer = center[0] + outer_tick_r * np.cos(tick_angle_rad)
    y_outer = center[1] + outer_tick_r * np.sin(tick_angle_rad)

    ax.plot([x_inner, x_outer], [y_inner, y_outer], color="#2C3E50", linewidth=2)

    # Labels
    x_label = center[0] + label_r * np.cos(tick_angle_rad)
    y_label = center[1] + label_r * np.sin(tick_angle_rad)
    ax.text(x_label, y_label, str(tick_val), ha="center", va="center", fontsize=18, fontweight="bold")

# Display current value prominently
ax.text(
    center[0], center[1] - 0.15, f"{value}", ha="center", va="center", fontsize=48, fontweight="bold", color="#2C3E50"
)

# Add label below value
ax.text(center[0], center[1] - 0.25, "Current Value", ha="center", va="center", fontsize=20, color="#7F8C8D")

# Set axis properties
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.8)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("gauge-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
