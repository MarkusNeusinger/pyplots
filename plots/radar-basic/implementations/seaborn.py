""" pyplots.ai
radar-basic: Basic Radar Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Employee performance comparison across competencies
categories = ["Communication", "Technical Skills", "Teamwork", "Leadership", "Problem Solving", "Creativity"]
employee_a = [85, 90, 75, 70, 88, 82]  # Senior Developer
employee_b = [78, 65, 92, 85, 72, 75]  # Team Lead

# Setup for radar chart
n_vars = len(categories)
angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

employee_a += employee_a[:1]
employee_b += employee_b[:1]

# Create polar plot with seaborn styling
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

# Python colors
color_blue = "#306998"
color_yellow = "#FFD43B"

# Plot data using matplotlib's polar plot with seaborn context
ax.fill(angles, employee_a, alpha=0.25, color=color_blue, label="Senior Developer")
ax.plot(angles, employee_a, color=color_blue, linewidth=3, marker="o", markersize=10)

ax.fill(angles, employee_b, alpha=0.25, color=color_yellow, label="Team Lead")
ax.plot(angles, employee_b, color=color_yellow, linewidth=3, marker="o", markersize=10)

# Configure axes
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=18)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=14, color="gray")

# Grid styling
ax.grid(True, alpha=0.3, linestyle="-")
ax.spines["polar"].set_visible(False)

# Title and legend
ax.set_title("radar-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=30)
ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), fontsize=16, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
