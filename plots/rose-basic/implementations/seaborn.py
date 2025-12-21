""" pyplots.ai
rose-basic: Basic Rose Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for better aesthetics
sns.set_theme(style="white")

# Data - Monthly rainfall (mm) showing seasonal patterns
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 52, 65, 89, 112, 145, 168, 155, 98, 76, 62, 71]

# Calculate angles for each month (equal spacing, starting at top)
n_categories = len(months)
angles = np.linspace(0, 2 * np.pi, n_categories, endpoint=False)

# Width of each bar (slightly less than full segment for visual separation)
width = 2 * np.pi / n_categories * 0.85

# Create polar plot with proper sizing
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection="polar")

# Create color palette using seaborn - Blues gradient based on values
colors = sns.color_palette("Blues", n_colors=n_categories)
# Map colors to values (darker = higher rainfall)
value_order = np.argsort(rainfall)
color_map = {i: colors[np.where(value_order == i)[0][0]] for i in range(n_categories)}
bar_colors = [color_map[i] for i in range(n_categories)]

# Plot bars with radius proportional to value
ax.bar(angles, rainfall, width=width, bottom=0, color=bar_colors, edgecolor="#306998", linewidth=2.5, alpha=0.85)

# Customize polar plot - start at top, go clockwise
ax.set_theta_offset(np.pi / 2)  # Start at top (12 o'clock)
ax.set_theta_direction(-1)  # Clockwise

# Set tick labels for months
ax.set_xticks(angles)
ax.set_xticklabels(months, fontsize=20, fontweight="bold")

# Configure radial gridlines and labels
ax.set_ylim(0, max(rainfall) * 1.15)
ax.set_yticks([50, 100, 150])
ax.set_yticklabels(["50 mm", "100 mm", "150 mm"], fontsize=16, color="#555555")

# Style the grid
ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#888888", linewidth=1.5)
ax.xaxis.grid(True, linestyle="-", alpha=0.3, color="#888888", linewidth=1)

# Remove outer spine for cleaner look
ax.spines["polar"].set_visible(False)

# Title
ax.set_title(
    "Monthly Rainfall · rose-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=25, color="#306998"
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
