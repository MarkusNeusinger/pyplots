""" pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


# Data - Simulated CPU usage monitoring with sliding window
np.random.seed(42)
n_points = 100
visible_points = 60

# Generate realistic CPU usage pattern (0-100%)
base_usage = 45 + 15 * np.sin(np.linspace(0, 4 * np.pi, n_points))
noise = np.random.normal(0, 5, n_points)
spikes = np.zeros(n_points)
spike_indices = [15, 35, 55, 78]
for idx in spike_indices:
    spikes[idx : idx + 3] = np.array([20, 15, 8])[: min(3, n_points - idx)]

cpu_usage = np.clip(base_usage + noise + spikes, 0, 100)

# Time axis (seconds ago, with most recent on right)
time_seconds = np.arange(n_points) * 0.1

# Visible window (last 60 points)
visible_time = time_seconds[-visible_points:]
visible_cpu = cpu_usage[-visible_points:]

# Current value for prominent display
current_value = visible_cpu[-1]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Create gradient fill effect using multiple fills with decreasing alpha
n_gradient = 10
for i in range(n_gradient):
    alpha_fill = 0.05 + 0.15 * (i / n_gradient)
    y_offset = visible_cpu * (1 - 0.02 * (n_gradient - i))
    ax.fill_between(visible_time, 0, y_offset, alpha=alpha_fill, color="#306998", linewidth=0)

# Main line with gradient effect (darker at right/newer)
colors = np.linspace(0.3, 1.0, visible_points)
for i in range(len(visible_time) - 1):
    ax.plot(
        visible_time[i : i + 2],
        visible_cpu[i : i + 2],
        color="#306998",
        alpha=colors[i],
        linewidth=3,
        solid_capstyle="round",
    )

# Fade effect on left edge (older data)
fade_width = 8
for i in range(fade_width):
    fade_alpha = 1 - (fade_width - i) / fade_width
    ax.axvspan(visible_time[i], visible_time[i + 1], alpha=0.3 * (1 - fade_alpha), color="white", zorder=2)

# Arrow indicating scroll direction (data flowing left)
arrow = FancyArrowPatch(
    (visible_time[5], 85),
    (visible_time[0], 85),
    arrowstyle="->",
    mutation_scale=25,
    color="#666666",
    linewidth=2,
    alpha=0.7,
)
ax.add_patch(arrow)
ax.text(visible_time[2], 90, "← older data", fontsize=14, color="#666666", ha="center")

# Current value indicator
ax.scatter([visible_time[-1]], [current_value], s=300, color="#FFD43B", zorder=5, edgecolor="#306998", linewidth=2)
ax.annotate(
    f"{current_value:.1f}%",
    (visible_time[-1], current_value),
    xytext=(15, 10),
    textcoords="offset points",
    fontsize=18,
    fontweight="bold",
    color="#306998",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "#FFD43B", "edgecolor": "#306998", "alpha": 0.9},
)

# Current time label
ax.text(visible_time[-1], -8, "NOW", fontsize=14, fontweight="bold", color="#306998", ha="center")

# Styling
ax.set_xlabel("Time (seconds)", fontsize=20)
ax.set_ylabel("CPU Usage (%)", fontsize=20)
ax.set_title("line-realtime · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Y-axis from 0 to 100 for CPU percentage
ax.set_ylim(-12, 105)
ax.set_xlim(visible_time[0] - 0.2, visible_time[-1] + 0.8)

# Grid
ax.grid(True, alpha=0.3, linestyle="--")

# Add horizontal threshold line
ax.axhline(y=80, color="#CC4444", linestyle="--", linewidth=2, alpha=0.6)
ax.text(visible_time[-1] + 0.3, 80, "Warning", fontsize=12, color="#CC4444", va="center")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
