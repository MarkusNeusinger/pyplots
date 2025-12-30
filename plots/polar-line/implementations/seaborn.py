"""pyplots.ai
polar-line: Polar Line Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")

# Data: Monthly average temperatures for two cities (cyclical pattern)
np.random.seed(42)
months = np.linspace(0, 2 * np.pi, 13)  # 12 months + closing point

# City A: Temperate climate with moderate seasonal variation
city_a_temps = np.array([5, 7, 12, 16, 20, 24, 26, 25, 21, 15, 9, 5, 5])

# City B: More extreme seasonal variation
city_b_temps = np.array([0, 2, 8, 14, 20, 26, 30, 29, 23, 14, 6, 1, 0])

# Create polar plot
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

# Use seaborn color palette
colors = sns.color_palette(["#306998", "#FFD43B"])

# Plot lines using seaborn-styled matplotlib
ax.plot(months, city_a_temps, color=colors[0], linewidth=3.5, marker="o", markersize=12, label="Coastal City")
ax.plot(months, city_b_temps, color=colors[1], linewidth=3.5, marker="s", markersize=12, label="Inland City")

# Fill area under curves with transparency
ax.fill(months, city_a_temps, color=colors[0], alpha=0.15)
ax.fill(months, city_b_temps, color=colors[1], alpha=0.15)

# Set month labels
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
ax.set_xticklabels(month_labels, fontsize=18)

# Style radial axis
ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])
ax.set_yticklabels(["0°C", "10°C", "20°C", "30°C"], fontsize=14)

# Title and legend
ax.set_title("Monthly Temperature Patterns · polar-line · seaborn · pyplots.ai", fontsize=22, pad=30, fontweight="bold")
ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), fontsize=16, frameon=True, fancybox=True)

# Customize grid
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_theta_zero_location("N")  # Start from top (January at 12 o'clock)
ax.set_theta_direction(-1)  # Clockwise direction

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
