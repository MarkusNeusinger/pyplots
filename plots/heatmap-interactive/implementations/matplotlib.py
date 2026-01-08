""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Server performance metrics matrix (15x20 for interactive exploration)
np.random.seed(42)

# Row labels: Servers (15 servers for clear exploration)
rows = [f"Server {i + 1:02d}" for i in range(15)]

# Column labels: Time periods (20 hours, 4AM-11PM)
cols = [f"{h:02d}:00" for h in range(4, 24)]

# Generate realistic server load data (0-100%)
# Base pattern: lower at night, peaks during business hours
hour_idx = np.arange(20)
hour_pattern = 20 + 60 * np.exp(-((hour_idx - 8) ** 2) / 30)  # Peak around noon (idx 8 = 12:00)
hour_pattern = hour_pattern / hour_pattern.max()

server_base = np.random.uniform(35, 85, size=15)

data = np.zeros((15, 20))
for i in range(15):
    data[i, :] = server_base[i] * hour_pattern + np.random.normal(0, 8, 20)

data = np.clip(data, 0, 100)  # Clamp to 0-100%

# Create plot with more height to fill canvas (3600x3600 square for heatmaps)
fig, ax = plt.subplots(figsize=(12, 12))

# Create heatmap with imshow - using viridis (colorblind-safe)
im = ax.imshow(data, cmap="viridis", aspect="auto", vmin=0, vmax=100)

# Set ticks and labels with proper sizing for square output
ax.set_xticks(np.arange(len(cols)))
ax.set_yticks(np.arange(len(rows)))
ax.set_xticklabels(cols, fontsize=14)
ax.set_yticklabels(rows, fontsize=14)

# Rotate x-axis labels for better readability
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add cell annotations showing exact values (simulating hover information)
# Threshold for viridis: values < 50 appear dark, >= 50 appear lighter
for i in range(len(rows)):
    for j in range(len(cols)):
        value = data[i, j]
        # Viridis goes from dark purple (low) to yellow (high)
        # Use white text on dark cells (low values), black on bright cells (high values)
        text_color = "white" if value < 50 else "black"
        ax.text(j, i, f"{value:.0f}", ha="center", va="center", fontsize=11, fontweight="bold", color=text_color)

# Add colorbar with proper sizing
cbar = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.02, aspect=30)
cbar.set_label("CPU Load (%)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Labels and title
ax.set_xlabel("Time of Day", fontsize=18)
ax.set_ylabel("Server", fontsize=18)
ax.set_title("heatmap-interactive · matplotlib · pyplots.ai", fontsize=22, pad=12)

# Add subtle cell borders using very thin lines (fixes VQ-07 - grid too prominent)
for i in range(len(rows) + 1):
    ax.axhline(y=i - 0.5, color="white", linewidth=0.5, alpha=0.2)
for j in range(len(cols) + 1):
    ax.axvline(x=j - 0.5, color="white", linewidth=0.5, alpha=0.2)

# Disable the minor tick grid system
ax.tick_params(which="minor", bottom=False, left=False)

# Add instruction text for interactivity context
fig.text(
    0.5,
    0.02,
    "Cell values shown | For interactive hover/zoom, see Plotly or Bokeh implementations",
    ha="center",
    fontsize=12,
    style="italic",
    color="gray",
)

plt.tight_layout(rect=[0, 0.04, 1, 1])  # Leave room for instruction text
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
