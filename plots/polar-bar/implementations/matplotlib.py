"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Wind rose showing wind direction frequencies with speed categories
np.random.seed(42)

# 8 compass directions
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
angles = np.linspace(0, 2 * np.pi, 9)[:-1]  # 8 directions, starting from N (top)
# Shift to put N at top (default 0 is at 3 o'clock, we want it at 12 o'clock)
angles = angles - np.pi / 2

# Wind speed categories (stacked bars for demonstration)
# Light (1-10 km/h), Moderate (10-20 km/h), Strong (20-30 km/h)
light = np.array([12, 8, 5, 3, 6, 15, 18, 10])  # More from W/NW
moderate = np.array([8, 5, 3, 2, 4, 10, 12, 7])
strong = np.array([4, 2, 1, 1, 2, 5, 6, 3])

# Bar width (slightly less than full sector for gaps)
width = 2 * np.pi / 8 * 0.8

# Plot - Create polar bar chart
_, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

# Stacked bars - bottom layer first
ax.bar(
    angles,
    light,
    width=width,
    bottom=0,
    color="#306998",
    alpha=0.9,
    label="Light (1-10 km/h)",
    edgecolor="white",
    linewidth=2,
)
ax.bar(
    angles,
    moderate,
    width=width,
    bottom=light,
    color="#FFD43B",
    alpha=0.9,
    label="Moderate (10-20 km/h)",
    edgecolor="white",
    linewidth=2,
)
ax.bar(
    angles,
    strong,
    width=width,
    bottom=light + moderate,
    color="#E55934",
    alpha=0.9,
    label="Strong (20-30 km/h)",
    edgecolor="white",
    linewidth=2,
)

# Styling
ax.set_theta_zero_location("N")  # Put 0 degrees at top
ax.set_theta_direction(-1)  # Clockwise
ax.set_xticks(angles + np.pi / 2)  # Adjust for our shift
ax.set_xticklabels(directions, fontsize=18, fontweight="bold")

# Radial labels (frequency)
ax.set_yticks([10, 20, 30, 40])
ax.set_yticklabels(["10%", "20%", "30%", "40%"], fontsize=14)
ax.set_ylim(0, 45)

# Grid styling
ax.grid(True, alpha=0.3, linestyle="--", linewidth=1.5)
ax.set_axisbelow(True)

# Title
ax.set_title("polar-bar · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=30)

# Legend
ax.legend(loc="lower right", fontsize=14, bbox_to_anchor=(1.15, -0.05), title="Wind Speed", title_fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
