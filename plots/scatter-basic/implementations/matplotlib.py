""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib 3.10.8 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - coffee shop daily sales: temperature vs iced drinks sold, colored by humidity
np.random.seed(42)
n_points = 150
temperature = np.random.uniform(5, 38, n_points)
base_sales = 10 + temperature * 2.8 + np.random.randn(n_points) * 12
iced_drinks = np.clip(base_sales, 5, 120).astype(float)
humidity = 30 + temperature * 0.8 + np.random.randn(n_points) * 15
humidity = np.clip(humidity, 15, 95)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9), facecolor="#fafafa")
ax.set_facecolor("#fafafa")

scatter = ax.scatter(
    temperature, iced_drinks, c=humidity, cmap="YlGnBu", s=90, alpha=0.75, edgecolors="white", linewidths=0.8, zorder=3
)

# Colorbar as distinctive matplotlib feature
cbar = fig.colorbar(scatter, ax=ax, pad=0.02, shrink=0.85, aspect=30)
cbar.set_label("Relative Humidity (%)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Labels and styling
ax.set_xlabel("Daily High Temperature (\u00b0C)", fontsize=20)
ax.set_ylabel("Iced Drinks Sold", fontsize=20)
ax.set_title("scatter-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, pad=15)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.25, linestyle="--", color="#888888", zorder=0)

# Refine spines
for spine in ax.spines.values():
    spine.set_color("#cccccc")
    spine.set_linewidth(0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
