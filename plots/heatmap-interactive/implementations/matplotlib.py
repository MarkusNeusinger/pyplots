"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Server performance metrics matrix (12x12 for optimal readability)
np.random.seed(42)

# Row labels: Servers
rows = [f"Server {i + 1:02d}" for i in range(12)]

# Column labels: Time periods (hours) - 6 AM to 5 PM (12 hours)
cols = [f"{h:02d}:00" for h in range(6, 18)]

# Generate realistic server load data (0-100%)
# Base pattern: higher load during business hours (peak 10 AM - 2 PM)
hour_pattern = np.array([0.3, 0.5, 0.7, 0.85, 0.95, 1.0, 0.95, 0.85, 0.7, 0.55, 0.4, 0.3])
server_base = np.random.uniform(40, 80, size=12)

data = np.zeros((12, 12))
for i in range(12):
    data[i, :] = server_base[i] * hour_pattern + np.random.normal(0, 10, 12)

data = np.clip(data, 0, 100)  # Clamp to 0-100%

# Create plot (16:9 aspect ratio for heatmap)
fig, ax = plt.subplots(figsize=(16, 9))

# Create heatmap with imshow - using viridis (colorblind-safe)
im = ax.imshow(data, cmap="viridis", aspect="auto", vmin=0, vmax=100)

# Set ticks and labels
ax.set_xticks(np.arange(len(cols)))
ax.set_yticks(np.arange(len(rows)))
ax.set_xticklabels(cols, fontsize=16)
ax.set_yticklabels(rows, fontsize=16)

# Rotate x-axis labels for better readability
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add cell annotations showing exact values
# Threshold for viridis: values < 50 appear dark, >= 50 appear lighter
for i in range(len(rows)):
    for j in range(len(cols)):
        value = data[i, j]
        # Viridis goes from dark purple (low) to yellow (high)
        # Use white text on dark cells (low values), black on bright cells (high values)
        text_color = "white" if value < 50 else "black"
        ax.text(j, i, f"{value:.0f}", ha="center", va="center", fontsize=14, fontweight="bold", color=text_color)

# Add colorbar with proper sizing
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("CPU Load (%)", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and title
ax.set_xlabel("Time of Day", fontsize=20)
ax.set_ylabel("Server", fontsize=20)
ax.set_title("heatmap-interactive · matplotlib · pyplots.ai", fontsize=24, pad=15)

# Add subtle grid lines between cells for visual separation
ax.set_xticks(np.arange(len(cols) + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(len(rows) + 1) - 0.5, minor=True)
ax.grid(which="minor", color="white", linestyle="-", linewidth=2, alpha=0.4)
ax.tick_params(which="minor", bottom=False, left=False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
