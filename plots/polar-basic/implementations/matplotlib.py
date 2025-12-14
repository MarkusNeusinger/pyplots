"""
polar-basic: Basic Polar Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Hourly temperature pattern (24-hour cycle)
np.random.seed(42)
hours = np.arange(24)
theta = hours * (2 * np.pi / 24)  # Convert hours to radians

# Simulated temperature pattern: warmer in afternoon, cooler at night
base_temp = 15 + 8 * np.sin(theta - np.pi / 2)  # Peak at 3 PM (hour 15)
noise = np.random.randn(24) * 1.5
radius = base_temp + noise

# Plot
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"projection": "polar"})

# Scatter points for hourly readings
ax.scatter(theta, radius, s=250, color="#306998", alpha=0.8, zorder=3, edgecolors="white", linewidth=2)

# Connect points with a line to show the pattern
ax.plot(np.append(theta, theta[0]), np.append(radius, radius[0]), color="#FFD43B", linewidth=3, alpha=0.7, zorder=2)

# Configure angular axis (hours of day)
ax.set_theta_zero_location("N")  # Start at top (midnight)
ax.set_theta_direction(-1)  # Clockwise
hour_labels = ["12 AM", "3 AM", "6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"]
ax.set_xticks(np.linspace(0, 2 * np.pi, 8, endpoint=False))
ax.set_xticklabels(hour_labels, fontsize=16)

# Configure radial axis (temperature)
ax.set_ylim(0, 30)
ax.set_yticks([5, 10, 15, 20, 25])
ax.set_yticklabels(["5°C", "10°C", "15°C", "20°C", "25°C"], fontsize=14)
ax.set_rlabel_position(45)

# Styling
ax.set_title("Hourly Temperature Pattern · polar-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
