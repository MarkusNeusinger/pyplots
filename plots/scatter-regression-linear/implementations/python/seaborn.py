""" anyplot.ai
scatter-regression-linear: Scatter Plot with Linear Regression
Library: seaborn 0.13.2 | Python 3.13.13
Quality: 93/100 | Updated: 2026-05-06
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# Theme tokens (see prompts/default-style-guide.md "Background" + "Theme-adaptive Chrome")
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
BRAND = "#009E73"  # Okabe-Ito position 1 — ALWAYS first series

# Configure seaborn theme
sns.set_theme(
    style="ticks",
    rc={
        "figure.facecolor": PAGE_BG,
        "axes.facecolor": PAGE_BG,
        "axes.edgecolor": INK_SOFT,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "grid.color": INK,
        "grid.alpha": 0.10,
        "legend.facecolor": ELEVATED_BG,
        "legend.edgecolor": INK_SOFT,
    },
)

# Data - Temperature vs energy consumption with realistic correlation
np.random.seed(42)
n_points = 100
temperature = np.random.uniform(5, 35, n_points)
energy_consumption = 50 + 2.5 * temperature + np.random.normal(0, 15, n_points)
energy_consumption = np.clip(energy_consumption, 20, 200)

# Calculate regression statistics
slope, intercept, r_value, p_value, std_err = stats.linregress(temperature, energy_consumption)
r_squared = r_value**2
y_pred = slope * temperature + intercept

# Compute 95% confidence interval using scipy
predict_se = np.sqrt(np.sum((energy_consumption - y_pred) ** 2) / (n_points - 2))
confidence_interval = 1.96 * predict_se

# Create figure and axis
fig, ax = plt.subplots(figsize=(16, 9))

# Plot scatter points with moderate transparency
ax.scatter(temperature, energy_consumption, s=180, alpha=0.6, color=BRAND, edgecolors="white", linewidth=1)

# Plot regression line
x_line = np.array([temperature.min(), temperature.max()])
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color=INK_SOFT, linewidth=3, linestyle="-", label="Linear Fit")

# Plot confidence band
ax.fill_between(x_line, y_line - confidence_interval, y_line + confidence_interval, alpha=0.2, color=BRAND)

# Add regression equation and R² annotation
equation_text = f"y = {slope:.2f}x + {intercept:.1f}\nR² = {r_squared:.3f}"
ax.annotate(
    equation_text,
    xy=(0.05, 0.95),
    xycoords="axes fraction",
    fontsize=18,
    verticalalignment="top",
    color=INK,
    bbox={"boxstyle": "round,pad=0.8", "facecolor": ELEVATED_BG, "alpha": 0.9, "edgecolor": INK_SOFT},
)

# Labels and styling
ax.set_xlabel("Temperature (°C)", fontsize=20, color=INK)
ax.set_ylabel("Energy Consumption (kWh)", fontsize=20, color=INK)
ax.set_title("Temperature vs Energy Consumption", fontsize=24, color=INK, pad=20)
ax.tick_params(axis="both", labelsize=16, colors=INK_SOFT)

# Grid styling
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8, color=INK)
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color(INK_SOFT)
ax.spines["bottom"].set_color(INK_SOFT)

# Set axis limits with padding
ax.set_xlim(0, 38)
ax.set_ylim(10, 210)

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
plt.close()
