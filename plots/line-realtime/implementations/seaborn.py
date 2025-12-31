"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter


# Data - Simulated CPU usage with realistic patterns
np.random.seed(42)
n_points = 100
visible_points = 60  # Sliding window shows last 60 points

# Create timestamps (100ms intervals)
base_time = pd.Timestamp("2025-12-31 14:30:00")
timestamps = pd.date_range(start=base_time, periods=n_points, freq="100ms")

# Generate realistic CPU usage (with spikes and trends)
base_usage = 45 + np.cumsum(np.random.randn(n_points) * 0.5)
spikes = np.random.choice([0, 15, 25], size=n_points, p=[0.85, 0.10, 0.05])
cpu_usage = np.clip(base_usage + spikes + np.random.randn(n_points) * 2, 5, 95)

# Create DataFrame
df = pd.DataFrame({"timestamp": timestamps, "cpu_usage": cpu_usage})

# Select visible window (sliding window effect)
df_visible = df.iloc[-visible_points:].copy()

# Create alpha gradient for fade effect (older points more transparent)
alpha_values = np.linspace(0.3, 1.0, visible_points)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Plot the main line with gradient effect (segment by segment for fade)
for i in range(len(df_visible) - 1):
    sns.lineplot(
        data=df_visible.iloc[i : i + 2],
        x="timestamp",
        y="cpu_usage",
        ax=ax,
        color="#306998",
        linewidth=3,
        alpha=alpha_values[i],
        legend=False,
    )

# Add scatter points at key locations (latest points more visible)
scatter_indices = [0, len(df_visible) // 4, len(df_visible) // 2, -10, -5, -1]
for idx in scatter_indices:
    point = df_visible.iloc[idx]
    alpha = alpha_values[idx] if idx >= 0 else 1.0
    size = 150 if idx == -1 else 80
    ax.scatter(
        point["timestamp"],
        point["cpu_usage"],
        s=size,
        color="#306998",
        alpha=alpha,
        zorder=5,
        edgecolors="white",
        linewidth=1.5,
    )

# Highlight the latest value with annotation
latest_value = df_visible.iloc[-1]["cpu_usage"]
latest_time = df_visible.iloc[-1]["timestamp"]
ax.annotate(
    f"Latest: {latest_value:.1f}%",
    xy=(latest_time, latest_value),
    xytext=(15, 25),
    textcoords="offset points",
    fontsize=18,
    fontweight="bold",
    color="#306998",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#FFD43B", "edgecolor": "#306998", "linewidth": 2},
    arrowprops={"arrowstyle": "->", "color": "#306998", "linewidth": 2},
)

# Add arrow indicating scroll direction (old data scrolls off left)
ax.annotate(
    "",
    xy=(df_visible.iloc[0]["timestamp"], 92),
    xytext=(df_visible.iloc[8]["timestamp"], 92),
    arrowprops={"arrowstyle": "<-", "color": "#666666", "linewidth": 2.5, "mutation_scale": 15},
)
ax.text(
    df_visible.iloc[4]["timestamp"],
    96,
    "← Old data scrolls off",
    fontsize=13,
    color="#666666",
    ha="center",
    style="italic",
)

# Styling
ax.set_xlabel("Time (HH:MM:SS)", fontsize=20)
ax.set_ylabel("CPU Usage (%)", fontsize=20)
ax.set_title("line-realtime · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Format x-axis time labels (cleaner format)
ax.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))
plt.xticks(rotation=25, ha="right")

# Set y-axis limits with padding
ax.set_ylim(0, 100)

# Grid styling
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_facecolor("#fafafa")

# Add live indicator with pulsing effect simulation
ax.text(
    0.02,
    0.96,
    "● LIVE",
    transform=ax.transAxes,
    fontsize=18,
    fontweight="bold",
    color="#e74c3c",
    verticalalignment="top",
)

# Add window info
ax.text(
    0.98,
    0.02,
    f"Sliding window: {visible_points} samples (6 sec)",
    transform=ax.transAxes,
    fontsize=13,
    color="#666666",
    ha="right",
    va="bottom",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
