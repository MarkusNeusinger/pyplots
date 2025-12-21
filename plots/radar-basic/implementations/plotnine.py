""" pyplots.ai
radar-basic: Basic Radar Chart
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - employee performance metrics
data = pd.DataFrame(
    {
        "category": ["Communication", "Technical Skills", "Teamwork", "Problem Solving", "Leadership", "Creativity"],
        "value": [85, 92, 78, 88, 72, 80],
    }
)

# Number of categories
n_cats = len(data)

# Compute angles for each axis (evenly spaced around the circle)
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()

# Close the polygon by repeating first point
values_closed = data["value"].tolist() + [data["value"].iloc[0]]
angles_closed = angles + [angles[0]]

# Create polar plot with plotnine-style sizing
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"polar": True})

# Draw filled polygon with Python Blue
ax.fill(angles_closed, values_closed, color="#306998", alpha=0.25)
ax.plot(angles_closed, values_closed, color="#306998", linewidth=3, marker="o", markersize=12)

# Set category labels at each axis
ax.set_xticks(angles)
ax.set_xticklabels(data["category"], fontsize=18)

# Set radial gridlines and labels (0-100 scale as recommended)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=14, color="gray")

# Grid styling - subtle, not dominant
ax.grid(True, linestyle="--", alpha=0.5, linewidth=1.5)

# Title in pyplots format
ax.set_title("radar-basic \u00b7 plotnine \u00b7 pyplots.ai", fontsize=24, pad=30)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
