""" pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch


# Data - simulated live server metrics with current and previous values
np.random.seed(42)
services = ["API Gateway", "Auth Service", "Database", "Cache", "Worker Queue", "CDN"]
current_values = [847, 623, 512, 389, 278, 156]  # Current requests/sec
previous_values = [792, 658, 498, 342, 295, 189]  # Previous snapshot

# Create DataFrames for seaborn
df_previous = pd.DataFrame({"Service": services, "Requests": previous_values, "State": "Previous"})
df_current = pd.DataFrame({"Service": services, "Requests": current_values, "State": "Current"})

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn barplot for the ghosted previous state (showing transition)
sns.barplot(
    data=df_previous,
    x="Service",
    y="Requests",
    hue="State",
    palette={"Previous": "#306998"},
    alpha=0.25,
    ax=ax,
    legend=False,
    width=0.6,
)

# Use seaborn barplot for current state (main bars)
sns.barplot(
    data=df_current,
    x="Service",
    y="Requests",
    hue="State",
    palette={"Current": "#306998"},
    alpha=0.85,
    ax=ax,
    legend=False,
    width=0.6,
    edgecolor="#1a3d5c",
    linewidth=2,
)

# Add value labels with change indicators (colorblind-friendly: blue/orange)
for i, (curr, prev) in enumerate(zip(current_values, previous_values, strict=True)):
    change = curr - prev
    change_pct = (change / prev) * 100 if prev > 0 else 0

    # Value label
    ax.text(i, curr + 25, f"{curr:,}", ha="center", va="bottom", fontsize=18, fontweight="bold", color="#1a3d5c")

    # Change indicator with arrow (colorblind-friendly colors)
    if change > 0:
        indicator = f"▲ +{change_pct:.1f}%"
        color = "#0072B2"  # Blue for increase
    elif change < 0:
        indicator = f"▼ {change_pct:.1f}%"
        color = "#D55E00"  # Orange for decrease
    else:
        indicator = "—"
        color = "#666666"

    ax.text(i, curr + 70, indicator, ha="center", va="bottom", fontsize=14, color=color, fontweight="medium")

# Add subtle motion lines to suggest animation/transition
for i, (curr, prev) in enumerate(zip(current_values, previous_values, strict=True)):
    if curr != prev:
        y_positions = np.linspace(min(curr, prev), max(curr, prev), 5)
        for y_pos in y_positions[1:-1]:
            ax.hlines(y_pos, i - 0.27, i + 0.27, colors="#306998", alpha=0.2, linewidth=1.5)

# Styling with seaborn
sns.despine(ax=ax, left=False, bottom=False)
ax.set_ylabel("Requests per Second", fontsize=20)
ax.set_xlabel("Service", fontsize=20)
ax.set_title("bar-realtime · seaborn · pyplots.ai", fontsize=24, pad=20)
ax.tick_params(axis="both", labelsize=16)

# Add grid for readability
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Custom legend for previous/current states
legend_elements = [
    Patch(facecolor="#306998", alpha=0.25, label="Previous State"),
    Patch(facecolor="#306998", alpha=0.85, edgecolor="#1a3d5c", linewidth=2, label="Current State"),
]
ax.legend(handles=legend_elements, fontsize=14, loc="upper right", framealpha=0.9)

# Add timestamp indicator to suggest live updates
ax.text(
    0.02, 0.98, "● LIVE", transform=ax.transAxes, fontsize=14, fontweight="bold", color="#e53935", va="top", ha="left"
)
ax.text(0.08, 0.98, " Last update: 0.8s ago", transform=ax.transAxes, fontsize=12, color="#666666", va="top", ha="left")

# Set y-axis limit with padding for labels
ax.set_ylim(0, max(current_values) * 1.2)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
