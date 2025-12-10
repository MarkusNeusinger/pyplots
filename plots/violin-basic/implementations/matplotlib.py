"""
violin-basic: Basic Violin Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Employee performance scores by department
np.random.seed(42)

departments = ["Engineering", "Sales", "Marketing", "Finance", "HR"]
data = [
    np.random.normal(75, 10, 150),  # Engineering
    np.concatenate([np.random.normal(65, 8, 80), np.random.normal(85, 5, 70)]),  # Sales (bimodal)
    np.random.normal(72, 12, 120),  # Marketing
    np.random.normal(80, 7, 100),  # Finance
    np.random.normal(70, 9, 90),  # HR
]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Violin plot with customization
parts = ax.violinplot(data, showmeans=False, showmedians=False, showextrema=False)

# Style the violin bodies
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(colors[i])
    pc.set_edgecolor("black")
    pc.set_linewidth(1.5)
    pc.set_alpha(0.7)

# Add inner box plot markers for quartiles and median
quartile1, medians, quartile3 = [], [], []
for d in data:
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    quartile1.append(q1)
    medians.append(med)
    quartile3.append(q3)

positions = range(1, len(departments) + 1)

# Draw quartile boxes
for i, pos in enumerate(positions):
    ax.vlines(pos, quartile1[i], quartile3[i], color="black", linewidth=5, zorder=3)
    ax.scatter(pos, medians[i], marker="o", color="white", s=40, zorder=4, edgecolors="black")

# Labels and styling
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Performance Score", fontsize=20)
ax.set_title("Employee Performance Distribution by Department", fontsize=20)

ax.set_xticks(positions)
ax.set_xticklabels(departments, fontsize=16)
ax.tick_params(axis="y", labelsize=16)

ax.grid(True, axis="y", alpha=0.3)
ax.set_ylim(30, 110)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
