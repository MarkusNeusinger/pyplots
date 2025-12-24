"""pyplots.ai
horizon-basic: Horizon Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Server metrics over 24 hours (5 servers)
np.random.seed(42)

hours = pd.date_range("2024-01-15 00:00", periods=96, freq="15min")  # 24 hours, 15-min intervals
servers = ["Web Server", "Database", "Cache", "API Gateway", "Auth Service"]

# Generate realistic CPU usage patterns with different characteristics
data = []
for server in servers:
    if server == "Web Server":
        # High during day, low at night with spikes
        base = 30 + 40 * np.sin(np.linspace(0, 2 * np.pi, 96)) ** 2
        noise = np.random.randn(96) * 8
        values = base + noise + np.random.choice([0, 30], 96, p=[0.95, 0.05])
    elif server == "Database":
        # Steady with occasional spikes
        base = np.ones(96) * 45
        noise = np.random.randn(96) * 10
        spikes = np.random.choice([0, 35], 96, p=[0.92, 0.08])
        values = base + noise + spikes
    elif server == "Cache":
        # Low baseline with periodic flushes
        base = np.ones(96) * 20
        flush_pattern = 25 * (np.arange(96) % 24 < 2).astype(float)
        noise = np.random.randn(96) * 5
        values = base + flush_pattern + noise
    elif server == "API Gateway":
        # Follows web server pattern but smoother
        base = 25 + 35 * np.sin(np.linspace(0, 2 * np.pi, 96)) ** 2
        noise = np.random.randn(96) * 6
        values = base + noise
    else:  # Auth Service
        # Low with login spikes in morning and evening
        base = np.ones(96) * 15
        morning_spike = 40 * np.exp(-((np.arange(96) - 32) ** 2) / 50)
        evening_spike = 30 * np.exp(-((np.arange(96) - 72) ** 2) / 50)
        noise = np.random.randn(96) * 4
        values = base + morning_spike + evening_spike + noise

    values = np.clip(values, 0, 100)  # CPU usage 0-100%
    for t, v in zip(hours, values, strict=True):
        data.append({"time": t, "server": server, "cpu_usage": v})

df = pd.DataFrame(data)

# Horizon chart parameters
n_bands = 3
band_height = 100 / n_bands  # Each band covers ~33.3% of the range

# Color bands - blue intensity increasing with magnitude
colors_positive = ["#a6cee3", "#1f78b4", "#08306b"]  # Light to dark blue

# Create figure
fig, axes = plt.subplots(len(servers), 1, figsize=(16, 9), sharex=True)
fig.subplots_adjust(hspace=0.05)

for idx, server in enumerate(servers):
    ax = axes[idx]
    server_data = df[df["server"] == server]
    x = np.arange(len(server_data))
    values = server_data["cpu_usage"].values

    # Clear axis
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, band_height)

    # Draw each band by folding values
    for band_idx in range(n_bands):
        band_min = band_idx * band_height
        band_max = (band_idx + 1) * band_height

        # Fold values into this band
        folded = np.clip(values - band_min, 0, band_height)

        # Only draw where there's data for this band
        mask = values > band_min
        if mask.any():
            ax.fill_between(x, 0, folded, color=colors_positive[band_idx], alpha=0.9, linewidth=0)

    # Style each row
    ax.set_ylabel(server, fontsize=14, rotation=0, ha="right", va="center", labelpad=10)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    if idx < len(servers) - 1:
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(bottom=False)

# X-axis formatting for bottom plot
time_labels = server_data["time"].dt.strftime("%H:%M")
tick_positions = np.arange(0, len(x), 16)  # Every 4 hours
axes[-1].set_xticks(tick_positions)
axes[-1].set_xticklabels([time_labels.iloc[i] for i in tick_positions], fontsize=14)
axes[-1].set_xlabel("Time (24-hour period)", fontsize=18)
axes[-1].tick_params(axis="x", labelsize=14)

# Title
fig.suptitle("Server CPU Usage · horizon-basic · seaborn · pyplots.ai", fontsize=22, y=0.98, fontweight="bold")

# Legend
legend_patches = [
    mpatches.Patch(color=colors_positive[0], label="0-33%"),
    mpatches.Patch(color=colors_positive[1], label="33-67%"),
    mpatches.Patch(color=colors_positive[2], label="67-100%"),
]
fig.legend(
    handles=legend_patches,
    loc="upper right",
    bbox_to_anchor=(0.98, 0.95),
    fontsize=14,
    title="CPU Usage",
    title_fontsize=14,
    framealpha=0.9,
)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
