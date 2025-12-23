""" pyplots.ai
violin-basic: Basic Violin Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulated test scores across different schools
np.random.seed(42)
categories = ["School A", "School B", "School C", "School D"]
data = [
    np.random.normal(75, 10, 150),  # School A: centered around 75
    np.random.normal(82, 8, 150),  # School B: higher scores, less spread
    np.random.normal(68, 15, 150),  # School C: lower average, more spread
    np.random.normal(78, 12, 150),  # School D: moderate
]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Create violin plot with quartile markers
parts = ax.violinplot(data, positions=range(len(categories)), showmeans=False, showmedians=True, showextrema=True)

# Style the violins with Python Blue
for pc in parts["bodies"]:
    pc.set_facecolor("#306998")
    pc.set_edgecolor("#1e4a6e")
    pc.set_alpha(0.7)
    pc.set_linewidth(2)

# Style the lines (median, min, max)
parts["cmedians"].set_color("#FFD43B")
parts["cmedians"].set_linewidth(3)
parts["cmins"].set_color("#1e4a6e")
parts["cmins"].set_linewidth(2)
parts["cmaxes"].set_color("#1e4a6e")
parts["cmaxes"].set_linewidth(2)
parts["cbars"].set_color("#1e4a6e")
parts["cbars"].set_linewidth(2)

# Add quartile markers (Q1 and Q3) as box indicators
quartile1 = [np.percentile(d, 25) for d in data]
quartile3 = [np.percentile(d, 75) for d in data]

# Draw thin boxes for interquartile range
for i, (q1, q3) in enumerate(zip(quartile1, quartile3, strict=True)):
    ax.vlines(i, q1, q3, color="#1e4a6e", linewidth=6, zorder=3)

# Labels and styling (scaled font sizes for 4800x2700)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
ax.set_xlabel("School", fontsize=20)
ax.set_ylabel("Test Score (points)", fontsize=20)
ax.set_title("violin-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
