"""pyplots.ai
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

# Apply seaborn styling with context for proper scaling
sns.set_theme(style="whitegrid", context="poster", font_scale=1.2)
palette = sns.color_palette("colorblind", 2)

# Create square figure for radar chart (3600x3600 at 300 dpi = 12x12 inches)
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

# Use seaborn colorblind-safe palette colors
color_senior = palette[0]
color_lead = palette[1]

# Plot filled polygons with seaborn-styled markers
ax.fill(angles, employee_a, alpha=0.25, color=color_senior, label="Senior Developer")
ax.plot(angles, employee_a, color=color_senior, linewidth=4, marker="o", markersize=14)

ax.fill(angles, employee_b, alpha=0.25, color=color_lead, label="Team Lead")
ax.plot(angles, employee_b, color=color_lead, linewidth=4, marker="o", markersize=14)

# Configure axes with larger tick labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=22, fontweight="medium")
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=18, color="gray")

# Style grid using seaborn's despine approach
ax.grid(True, alpha=0.3, linestyle="-", linewidth=1.5)
ax.spines["polar"].set_visible(False)

# Title with proper padding
ax.set_title("radar-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=35)

# Legend positioned within the figure bounds
ax.legend(
    loc="upper left", bbox_to_anchor=(0.95, 0.95), fontsize=18, framealpha=0.95, edgecolor="lightgray", fancybox=True
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
