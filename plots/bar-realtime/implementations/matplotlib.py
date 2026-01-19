"""pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulated real-time monitoring metrics (current snapshot)
np.random.seed(42)
categories = ["Server A", "Server B", "Server C", "Server D", "Server E", "Server F"]
current_values = np.array([78, 92, 45, 88, 63, 71])  # Current CPU usage %

# Previous values for "ghost" effect showing recent history
previous_values_1 = current_values - np.random.randint(-8, 12, size=len(categories))
previous_values_2 = previous_values_1 - np.random.randint(-8, 12, size=len(categories))
previous_values_1 = np.clip(previous_values_1, 0, 100)
previous_values_2 = np.clip(previous_values_2, 0, 100)


# Colors based on thresholds (green < 60, yellow 60-80, red > 80)
def get_color(val):
    if val > 80:
        return "#E74C3C"  # Red - critical
    elif val > 60:
        return "#F39C12"  # Orange/Yellow - warning
    else:
        return "#27AE60"  # Green - normal


colors = [get_color(v) for v in current_values]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

x = np.arange(len(categories))
bar_width = 0.6

# Draw ghosted previous states (motion blur effect)
ax.bar(x, previous_values_2, width=bar_width, color="#AAAAAA", alpha=0.3, edgecolor="none")
ax.bar(x, previous_values_1, width=bar_width, color="#888888", alpha=0.4, edgecolor="none")

# Draw current bars
bars = ax.bar(x, current_values, width=bar_width, color=colors, alpha=0.9, edgecolor="#333333", linewidth=1.5)

# Value labels on bars
for bar, val in zip(bars, current_values, strict=True):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        f"{val}%",
        ha="center",
        va="bottom",
        fontsize=18,
        fontweight="bold",
        color="#333333",
    )

# Change indicators (arrows showing trend)
for i, (curr, prev) in enumerate(zip(current_values, previous_values_1, strict=True)):
    change = curr - prev
    if change > 0:
        arrow = "▲"
        arrow_color = "#E74C3C"
    elif change < 0:
        arrow = "▼"
        arrow_color = "#27AE60"
    else:
        arrow = "●"
        arrow_color = "#888888"
    ax.text(x[i], curr + 8, arrow, ha="center", va="bottom", fontsize=14, color=arrow_color, alpha=0.8)

# Threshold lines
ax.axhline(y=80, color="#E74C3C", linestyle="--", linewidth=2, alpha=0.5, label="Critical (80%)")
ax.axhline(y=60, color="#F39C12", linestyle="--", linewidth=2, alpha=0.5, label="Warning (60%)")

# Styling
ax.set_xlabel("Monitoring Target", fontsize=20)
ax.set_ylabel("CPU Usage (%)", fontsize=20)
ax.set_title("bar-realtime · matplotlib · pyplots.ai", fontsize=24)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=16)
ax.tick_params(axis="y", labelsize=16)
ax.set_ylim(0, 110)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")
ax.legend(fontsize=14, loc="upper right")

# Add "LIVE" indicator to show real-time nature
ax.text(
    0.02,
    0.98,
    "● LIVE",
    transform=ax.transAxes,
    fontsize=16,
    fontweight="bold",
    color="#E74C3C",
    va="top",
    ha="left",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#E74C3C", "alpha": 0.9},
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
