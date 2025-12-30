"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

# Create realistic data: Plant growth experiment across conditions
# Row variable: Light Level (Low, Medium, High)
# Column variable: Soil Type (Sandy, Loamy, Clay)
light_levels = ["Low", "Medium", "High"]
soil_types = ["Sandy", "Loamy", "Clay"]

data = []
for light in light_levels:
    for soil in soil_types:
        # Base growth varies by light and soil
        light_effect = {"Low": 5, "Medium": 15, "High": 25}[light]
        soil_effect = {"Sandy": -2, "Loamy": 5, "Clay": 0}[soil]
        base = light_effect + soil_effect

        # Generate 30 points per condition
        n = 30
        days = np.linspace(1, 30, n) + np.random.uniform(-0.5, 0.5, n)
        growth = base + days * 0.5 + np.random.normal(0, 2, n)
        growth = np.maximum(growth, 0)  # No negative growth

        for d, g in zip(days, growth, strict=True):
            data.append({"Days": d, "Growth (cm)": g, "Light": light, "Soil": soil})

df = pd.DataFrame(data)

# Create faceted grid: 3 rows (Light) x 3 columns (Soil)
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(16, 9), sharex=True, sharey=True, squeeze=False)

# Python colors
color_main = "#306998"
color_accent = "#FFD43B"

# Plot each facet
for i, light in enumerate(light_levels):
    for j, soil in enumerate(soil_types):
        ax = axes[i, j]
        subset = df[(df["Light"] == light) & (df["Soil"] == soil)]

        ax.scatter(
            subset["Days"], subset["Growth (cm)"], s=100, alpha=0.7, color=color_main, edgecolors="white", linewidth=0.5
        )

        # Add trend line
        z = np.polyfit(subset["Days"], subset["Growth (cm)"], 1)
        p = np.poly1d(z)
        x_line = np.linspace(subset["Days"].min(), subset["Days"].max(), 50)
        ax.plot(x_line, p(x_line), color=color_accent, linewidth=2.5, alpha=0.9)

        # Facet title
        ax.set_title(f"{light} Light | {soil} Soil", fontsize=14, fontweight="bold")

        # Grid
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.tick_params(axis="both", labelsize=12)

# Shared axis labels
fig.text(0.5, 0.02, "Days", ha="center", fontsize=20)
fig.text(0.02, 0.5, "Growth (cm)", va="center", rotation="vertical", fontsize=20)

# Main title
fig.suptitle("facet-grid · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0.04, 0.05, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
