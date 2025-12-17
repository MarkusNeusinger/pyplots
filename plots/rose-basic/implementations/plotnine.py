"""
rose-basic: Basic Rose Chart
Library: plotnine

Note: plotnine doesn't support coord_polar for rose charts.
Using matplotlib directly with plotnine-style aesthetics.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Monthly rainfall (mm) showing natural 12-month cycle
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "rainfall": [78, 52, 65, 45, 38, 25, 18, 22, 42, 68, 85, 92],
    }
)

n_cats = len(data)

# Compute angles - equal spacing for each month
# Start at top (12 o'clock) which is pi/2, but we need to offset for bar width
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False)
width = 2 * np.pi / n_cats  # Width of each wedge

# Values (rainfall) determine radius
values = data["rainfall"].values

# Colors - Python Blue with slight variation for visual interest
colors = ["#306998"] * n_cats

# Create polar plot with plotnine-style sizing
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"polar": True})

# Start at top (12 o'clock position) and go clockwise
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw rose petals (bars in polar coordinates)
bars = ax.bar(
    angles,
    values,
    width=width * 0.9,  # Slight gap between bars
    color=colors,
    alpha=0.8,
    edgecolor="#1a3a52",
    linewidth=2,
)

# Add Python Yellow accent for the highest value
max_idx = np.argmax(values)
bars[max_idx].set_facecolor("#FFD43B")
bars[max_idx].set_alpha(0.9)

# Set category labels (months)
ax.set_xticks(angles)
ax.set_xticklabels(data["month"], fontsize=18, fontweight="bold")

# Set radial gridlines and labels
max_val = max(values)
tick_vals = [25, 50, 75, 100]
ax.set_ylim(0, 105)
ax.set_yticks(tick_vals)
ax.set_yticklabels([f"{v} mm" for v in tick_vals], fontsize=14, color="gray")

# Grid styling - subtle radial gridlines
ax.grid(True, linestyle="--", alpha=0.4, linewidth=1.5)

# Title in pyplots format
ax.set_title("Monthly Rainfall · rose-basic · plotnine · pyplots.ai", fontsize=24, fontweight="bold", pad=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
