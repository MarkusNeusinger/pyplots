""" pyplots.ai
horizon-basic: Horizon Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-24
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seaborn style
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.0)

# Data - Server metrics over 24 hours (5 servers)
np.random.seed(42)

hours = pd.date_range("2024-01-15 00:00", periods=96, freq="15min")  # 24 hours, 15-min intervals
servers = ["Web Server", "Database", "Cache", "API Gateway", "Auth Service"]

# Generate realistic CPU usage patterns with deviations from baseline (positive and negative)
# Baseline is 50% CPU, deviations show above/below normal operation
data = []
for server in servers:
    if server == "Web Server":
        # High during day, low at night - deviation from 50% baseline
        base = 40 * np.sin(np.linspace(0, 2 * np.pi, 96)) ** 2 - 10
        noise = np.random.randn(96) * 8
        values = base + noise + np.random.choice([0, 25], 96, p=[0.95, 0.05])
    elif server == "Database":
        # Steady with occasional positive and negative spikes
        base = np.zeros(96)
        noise = np.random.randn(96) * 12
        spikes = np.random.choice([-30, 0, 35], 96, p=[0.05, 0.87, 0.08])
        values = base + noise + spikes
    elif server == "Cache":
        # Low baseline with periodic flush spikes
        base = np.ones(96) * -15
        flush_pattern = 35 * (np.arange(96) % 24 < 2).astype(float)
        noise = np.random.randn(96) * 5
        values = base + flush_pattern + noise
    elif server == "API Gateway":
        # Follows web server pattern but smoother
        base = 35 * np.sin(np.linspace(0, 2 * np.pi, 96)) ** 2 - 8
        noise = np.random.randn(96) * 6
        values = base + noise
    else:  # Auth Service
        # Low with login spikes in morning and evening, dips at night
        base = np.ones(96) * -10
        morning_spike = 40 * np.exp(-((np.arange(96) - 32) ** 2) / 50)
        evening_spike = 30 * np.exp(-((np.arange(96) - 72) ** 2) / 50)
        night_dip = -20 * np.exp(-((np.arange(96) - 10) ** 2) / 30)
        noise = np.random.randn(96) * 4
        values = base + morning_spike + evening_spike + night_dip + noise

    values = np.clip(values, -50, 50)  # Deviation from baseline: -50% to +50%
    for t, v in zip(hours, values, strict=True):
        data.append({"time": t, "server": server, "deviation": v})

df = pd.DataFrame(data)

# Horizon chart parameters
n_bands = 3
band_height = 50 / n_bands  # Each band covers ~16.7% of the range (0-50 for each direction)

# Create figure
fig, axes = plt.subplots(len(servers), 1, figsize=(16, 9), sharex=True)
fig.subplots_adjust(hspace=0.08)

for idx, server in enumerate(servers):
    ax = axes[idx]
    server_data = df[df["server"] == server]
    x = np.arange(len(server_data))
    values = server_data["deviation"].values

    # Clear axis
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, band_height)

    # Separate positive and negative values
    positive_vals = np.maximum(values, 0)
    negative_vals = np.abs(np.minimum(values, 0))

    # Get seaborn color palettes
    blue_palette = sns.color_palette("Blues", n_colors=n_bands + 2)[2:]  # Skip lightest colors
    red_palette = sns.color_palette("Reds", n_colors=n_bands + 2)[2:]  # Skip lightest colors

    # Draw horizon bands - each point is either positive or negative, not both
    # Draw from highest band to lowest so layering works correctly
    for band_idx in range(n_bands - 1, -1, -1):
        band_min = band_idx * band_height

        # Positive bands (blue) - only where values are positive
        pos_folded = np.clip(positive_vals - band_min, 0, band_height)
        pos_mask = positive_vals > band_min
        pos_y = np.where(pos_mask, pos_folded, 0)
        ax.fill_between(x, 0, pos_y, color=blue_palette[band_idx], alpha=0.9, linewidth=0)

        # Negative bands (red) - only where values are negative (shown as absolute magnitude)
        neg_folded = np.clip(negative_vals - band_min, 0, band_height)
        neg_mask = negative_vals > band_min
        neg_y = np.where(neg_mask, neg_folded, 0)
        ax.fill_between(x, 0, neg_y, color=red_palette[band_idx], alpha=0.9, linewidth=0)

    # Style each row - use seaborn's despine for cleaner look
    ax.set_ylabel(server, fontsize=16, rotation=0, ha="right", va="center", labelpad=15)
    ax.set_yticks([])

    # Add subtle grid lines for tracking
    ax.grid(True, axis="x", alpha=0.3, linewidth=0.5, color="#cccccc")
    ax.set_axisbelow(True)

    sns.despine(ax=ax, left=True, right=True, top=True, bottom=(idx < len(servers) - 1))
    if idx < len(servers) - 1:
        ax.tick_params(bottom=False)

# X-axis formatting for bottom plot
time_labels = server_data["time"].dt.strftime("%H:%M")
tick_positions = np.arange(0, len(x), 16)  # Every 4 hours
axes[-1].set_xticks(tick_positions)
axes[-1].set_xticklabels([time_labels.iloc[i] for i in tick_positions], fontsize=16)
axes[-1].set_xlabel("Time (24-hour period)", fontsize=20)
axes[-1].tick_params(axis="x", labelsize=16)

# Title - correct format per SC-06
fig.suptitle("horizon-basic · seaborn · pyplots.ai", fontsize=24, y=0.98, fontweight="bold")

# Legend with both positive and negative indicators - create palettes again for legend
legend_blue = sns.color_palette("Blues", n_colors=n_bands + 2)[2:]
legend_red = sns.color_palette("Reds", n_colors=n_bands + 2)[2:]
legend_patches = [
    mpatches.Patch(color=legend_blue[0], label="0-17% above"),
    mpatches.Patch(color=legend_blue[1], label="17-33% above"),
    mpatches.Patch(color=legend_blue[2], label="33-50% above"),
    mpatches.Patch(color=legend_red[0], label="0-17% below"),
    mpatches.Patch(color=legend_red[1], label="17-33% below"),
    mpatches.Patch(color=legend_red[2], label="33-50% below"),
]
fig.legend(
    handles=legend_patches,
    loc="upper right",
    bbox_to_anchor=(0.98, 0.92),
    fontsize=14,
    title="Deviation from Baseline",
    title_fontsize=14,
    framealpha=0.9,
    ncol=2,
)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
