"""
radar-basic: Basic Radar Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Employee performance evaluation across competencies
categories = ["Communication", "Technical Skills", "Teamwork", "Problem Solving", "Leadership", "Creativity"]
values = [85, 90, 78, 88, 72, 80]

# Number of variables
num_vars = len(categories)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Close the polygon by appending first value
values_closed = values + [values[0]]
angles_closed = angles + [angles[0]]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"polar": True})

# Plot data
ax.fill(angles_closed, values_closed, color="#306998", alpha=0.25)
ax.plot(angles_closed, values_closed, color="#306998", linewidth=3, marker="o", markersize=12)

# Set the angle for each axis label
ax.set_xticks(angles)
ax.set_xticklabels(categories, fontsize=18)

# Set radial limits and gridlines
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=14, color="gray")

# Style grid
ax.grid(True, alpha=0.4, linestyle="--", linewidth=1.5)

# Title
ax.set_title("radar-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
