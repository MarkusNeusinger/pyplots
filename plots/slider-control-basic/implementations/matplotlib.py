"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-01
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


# Data - Monthly temperature readings across multiple years
np.random.seed(42)
years = np.arange(2015, 2025)
months = np.arange(1, 13)

# Generate realistic temperature data (seasonal pattern with yearly variation)
base_temps = 15 + 12 * np.sin((months - 4) * np.pi / 6)  # Seasonal pattern
all_data = {}
for year in years:
    yearly_offset = (year - 2020) * 0.3  # Slight warming trend
    noise = np.random.normal(0, 2, 12)
    all_data[year] = base_temps + yearly_offset + noise

# Create figure with space for slider
fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(bottom=0.2)

# Initial plot for first year
initial_year = years[0]
(line,) = ax.plot(
    months,
    all_data[initial_year],
    marker="o",
    markersize=12,
    linewidth=3,
    color="#306998",
    markerfacecolor="#FFD43B",
    markeredgecolor="#306998",
    markeredgewidth=2,
)

# Fill area under curve
fill = ax.fill_between(months, all_data[initial_year], alpha=0.2, color="#306998")

# Styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Temperature (°C)", fontsize=20)
ax.set_title("slider-control-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)
ax.set_xticks(months)
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fontsize=14)
ax.set_ylim(-5, 35)
ax.set_xlim(0.5, 12.5)
ax.grid(True, alpha=0.3, linestyle="--")

# Year display text
year_text = ax.text(
    0.98,
    0.95,
    f"Year: {initial_year}",
    transform=ax.transAxes,
    fontsize=28,
    fontweight="bold",
    ha="right",
    va="top",
    color="#306998",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "#FFD43B", "edgecolor": "#306998", "linewidth": 2},
)

# Create slider axis
slider_ax = plt.axes([0.2, 0.05, 0.6, 0.04])
year_slider = Slider(
    ax=slider_ax, label="Year", valmin=years.min(), valmax=years.max(), valinit=initial_year, valstep=1, color="#306998"
)
year_slider.label.set_fontsize(18)
year_slider.valtext.set_fontsize(16)


# Update function for slider
def update(val):
    year = int(year_slider.val)
    line.set_ydata(all_data[year])
    year_text.set_text(f"Year: {year}")
    # Update fill - need to remove old and add new
    global fill
    fill.remove()
    fill = ax.fill_between(months, all_data[year], alpha=0.2, color="#306998")
    fig.canvas.draw_idle()


year_slider.on_changed(update)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
