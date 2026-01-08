""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 90/100 | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Server performance metrics matrix (12x16 for clear display with annotations)
np.random.seed(42)

# Row labels: Servers (12 servers for clear exploration)
rows = [f"Server {i + 1:02d}" for i in range(12)]

# Column labels: Time periods (16 hours, 6AM-9PM)
cols = [f"{h:02d}:00" for h in range(6, 22)]

# Generate realistic server load data (0-100%)
# Base pattern: lower at night, peaks during business hours
hour_idx = np.arange(16)
hour_pattern = 20 + 60 * np.exp(-((hour_idx - 6) ** 2) / 25)  # Peak around noon (idx 6 = 12:00)
hour_pattern = hour_pattern / hour_pattern.max()

server_base = np.random.uniform(35, 85, size=12)

data = np.zeros((12, 16))
for i in range(12):
    data[i, :] = server_base[i] * hour_pattern + np.random.normal(0, 8, 16)

data = np.clip(data, 0, 100)  # Clamp to 0-100%

# Create plot with landscape format (4800x2700 at dpi=300 = 16x9 inches)
fig, ax = plt.subplots(figsize=(16, 9))

# Create heatmap with imshow - using viridis (colorblind-safe)
im = ax.imshow(data, cmap="viridis", aspect="auto", vmin=0, vmax=100)

# Set ticks and labels with proper sizing
ax.set_xticks(np.arange(len(cols)))
ax.set_yticks(np.arange(len(rows)))
ax.set_xticklabels(cols, fontsize=16)
ax.set_yticklabels(rows, fontsize=16)

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
        ax.text(j, i, f"{value:.0f}", ha="center", va="center", fontsize=14, fontweight="bold", color=text_color)

# Add colorbar with proper sizing
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02, aspect=25)
cbar.set_label("CPU Load (%)", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and title
ax.set_xlabel("Time of Day", fontsize=20)
ax.set_ylabel("Server", fontsize=20)
ax.set_title("heatmap-interactive · matplotlib · pyplots.ai", fontsize=24, pad=15)

# Remove grid entirely for cleaner appearance - cell colors provide enough visual separation
ax.tick_params(which="both", bottom=False, left=False)

# Add instruction text for interactivity context
fig.text(
    0.5,
    0.01,
    "Cell values shown | For interactive hover/zoom, see Plotly or Bokeh implementations",
    ha="center",
    fontsize=14,
    style="italic",
    color="gray",
)

plt.tight_layout(rect=[0, 0.03, 1, 1])  # Leave room for instruction text
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
