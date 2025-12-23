"""pyplots.ai
gauge-basic: Basic Gauge Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="white", font_scale=1.2)

# Data - Sales performance gauge
value = 72  # Current sales performance
min_value = 0
max_value = 100
thresholds = [30, 70]  # Red < 30, Yellow 30-70, Green > 70

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Gauge parameters
center = (0.5, 0.35)
radius = 0.35
width = 0.15
start_angle = 180  # Left side
end_angle = 0  # Right side

# Color zones using seaborn palette colors
colors = ["#E74C3C", "#F39C12", "#27AE60"]  # Red, Yellow, Green

# Calculate angle ranges for each zone
angle_range = start_angle - end_angle  # 180 degrees
value_range = max_value - min_value

# Draw gauge segments (background arcs)
zone_boundaries = [min_value] + thresholds + [max_value]
for i in range(len(zone_boundaries) - 1):
    zone_start = zone_boundaries[i]
    zone_end = zone_boundaries[i + 1]

    # Convert value range to angle range
    theta1 = start_angle - (zone_end - min_value) / value_range * angle_range
    theta2 = start_angle - (zone_start - min_value) / value_range * angle_range

    wedge = mpatches.Wedge(
        center, radius, theta1, theta2, width=width, facecolor=colors[i], edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)

# Draw needle
needle_angle = start_angle - (value - min_value) / value_range * angle_range
needle_rad = np.radians(needle_angle)

# Needle base and tip
needle_length = radius - width / 2
needle_tip_x = center[0] + needle_length * np.cos(needle_rad)
needle_tip_y = center[1] + needle_length * np.sin(needle_rad)

# Draw needle as a thick line with arrow
ax.annotate(
    "",
    xy=(needle_tip_x, needle_tip_y),
    xytext=center,
    arrowprops={"arrowstyle": "-|>", "color": "#306998", "lw": 4, "mutation_scale": 20},
)

# Draw center circle
center_circle = plt.Circle(center, 0.04, color="#306998", zorder=5)
ax.add_patch(center_circle)

# Add value display
ax.text(
    center[0], center[1] - 0.18, f"{value}%", ha="center", va="center", fontsize=48, fontweight="bold", color="#306998"
)

# Add min and max labels
ax.text(
    center[0] - radius + width / 2,
    center[1] - 0.08,
    f"{min_value}",
    ha="center",
    va="top",
    fontsize=20,
    color="#555555",
)
ax.text(
    center[0] + radius - width / 2,
    center[1] - 0.08,
    f"{max_value}",
    ha="center",
    va="top",
    fontsize=20,
    color="#555555",
)

# Add zone labels inside the arcs
# Calculate positions on the gauge at the center of each zone
zone_angles = [
    start_angle - (15 / value_range) * angle_range,  # Center of Low (0-30), at 15
    start_angle - (50 / value_range) * angle_range,  # Center of Medium (30-70), at 50
    start_angle - (85 / value_range) * angle_range,  # Center of High (70-100), at 85
]
label_radius = radius - width / 2  # Place labels on the arc
zone_labels = ["Low", "Medium", "High"]
zone_colors = ["white", "white", "white"]

for angle, label, color in zip(zone_angles, zone_labels, zone_colors, strict=True):
    rad = np.radians(angle)
    x = center[0] + label_radius * np.cos(rad)
    y = center[1] + label_radius * np.sin(rad)
    ax.text(x, y, label, ha="center", va="center", fontsize=14, color=color, fontweight="bold")

# Add title
ax.set_title("gauge-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=20, color="#333333")

# Add subtitle
ax.text(center[0], 0.92, "Sales Performance", ha="center", va="top", fontsize=22, color="#555555")

# Set axis properties
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
