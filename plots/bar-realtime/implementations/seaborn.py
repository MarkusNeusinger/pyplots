"""pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulated live server metrics with current and previous values
np.random.seed(42)
categories = ["API Gateway", "Auth Service", "Database", "Cache", "Worker Queue", "CDN"]
current_values = [847, 623, 512, 389, 278, 156]  # Current requests/sec
previous_values = [792, 658, 498, 342, 295, 189]  # Previous snapshot

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Bar positions
x = np.arange(len(categories))
bar_width = 0.6

# Draw ghosted previous state bars (showing motion/transition)
bars_ghost = ax.bar(
    x, previous_values, width=bar_width, color="#306998", alpha=0.25, edgecolor="none", label="Previous State"
)

# Draw current state bars
bars_current = ax.bar(
    x,
    current_values,
    width=bar_width,
    color="#306998",
    alpha=0.85,
    edgecolor="#1a3d5c",
    linewidth=2,
    label="Current State",
)

# Add value labels with change indicators
for i, (curr, prev) in enumerate(zip(current_values, previous_values, strict=True)):
    change = curr - prev
    change_pct = (change / prev) * 100 if prev > 0 else 0

    # Value label
    ax.text(i, curr + 25, f"{curr:,}", ha="center", va="bottom", fontsize=18, fontweight="bold", color="#1a3d5c")

    # Change indicator with arrow
    if change > 0:
        indicator = f"▲ +{change_pct:.1f}%"
        color = "#2d8a4e"
    elif change < 0:
        indicator = f"▼ {change_pct:.1f}%"
        color = "#c94c4c"
    else:
        indicator = "—"
        color = "#666666"

    ax.text(i, curr + 70, indicator, ha="center", va="bottom", fontsize=14, color=color, fontweight="medium")

# Add motion blur effect lines to suggest animation
for i, (curr, prev) in enumerate(zip(current_values, previous_values, strict=True)):
    if curr != prev:
        # Draw subtle transition lines
        y_positions = np.linspace(min(curr, prev), max(curr, prev), 4)
        for y_pos in y_positions[1:-1]:
            ax.hlines(y_pos, i - bar_width / 2.2, i + bar_width / 2.2, colors="#306998", alpha=0.15, linewidth=1)

# Styling
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=16)
ax.set_ylabel("Requests per Second", fontsize=20)
ax.set_xlabel("Service", fontsize=20)
ax.set_title("bar-realtime · seaborn · pyplots.ai", fontsize=24, pad=20)
ax.tick_params(axis="y", labelsize=16)

# Add grid for readability
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Legend
ax.legend(fontsize=14, loc="upper right", framealpha=0.9)

# Add timestamp indicator to suggest live updates
ax.text(
    0.02, 0.98, "● LIVE", transform=ax.transAxes, fontsize=14, fontweight="bold", color="#e53935", va="top", ha="left"
)

ax.text(0.08, 0.98, " Last update: 0.8s ago", transform=ax.transAxes, fontsize=12, color="#666666", va="top", ha="left")

# Set y-axis limit with padding for labels
ax.set_ylim(0, max(current_values) * 1.25)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
