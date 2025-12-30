"""pyplots.ai
polar-line: Polar Line Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data: Simulating wind speed patterns over 24 hours at a weather station
np.random.seed(42)

# Hours of the day converted to radians (0-24 hours -> 0-2π)
hours = np.arange(0, 24, 1)
theta = hours * (2 * np.pi / 24)

# Wind speed patterns (m/s) - morning calm, afternoon peak, evening decline
base_pattern = 3 + 4 * np.sin((hours - 6) * np.pi / 12)  # Peak around 2-3 PM
noise = np.random.uniform(-0.5, 0.5, len(hours))
wind_speed = np.clip(base_pattern + noise, 0.5, 10)

# Second series: Previous day for comparison
wind_speed_prev = np.clip(base_pattern + np.random.uniform(-1, 1, len(hours)), 0.5, 10)

# Close the loop by appending the first point at the end
theta_closed = np.append(theta, theta[0])
wind_speed_closed = np.append(wind_speed, wind_speed[0])
wind_speed_prev_closed = np.append(wind_speed_prev, wind_speed_prev[0])

# Create polar plot (square format works better for polar plots)
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

# Plot both series
ax.plot(
    theta_closed, wind_speed_closed, linewidth=3, color="#306998", label="Today", marker="o", markersize=10, alpha=0.9
)
ax.plot(
    theta_closed,
    wind_speed_prev_closed,
    linewidth=3,
    color="#FFD43B",
    label="Yesterday",
    marker="s",
    markersize=8,
    alpha=0.8,
)

# Configure angular axis (theta) - hours of the day
hour_labels = ["12 AM", "3 AM", "6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"]
ax.set_xticks(np.linspace(0, 2 * np.pi, 8, endpoint=False))
ax.set_xticklabels(hour_labels, fontsize=16)

# Configure radial axis
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2 m/s", "4 m/s", "6 m/s", "8 m/s", "10 m/s"], fontsize=14)

# Style the plot
ax.set_title("polar-line · matplotlib · pyplots.ai", fontsize=24, pad=30, fontweight="bold")
ax.legend(loc="upper right", fontsize=16, bbox_to_anchor=(1.15, 1.1))
ax.grid(True, alpha=0.3, linestyle="--")

# Set starting position at top (12 AM)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)  # Clockwise

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
