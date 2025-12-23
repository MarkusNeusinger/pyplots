""" pyplots.ai
bump-basic: Basic Bump Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Sports league standings over a season
entities = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon"]
periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]

# Rankings for each team across periods (1 = best)
rankings = {
    "Team Alpha": [3, 2, 1, 1, 2, 1],
    "Team Beta": [1, 1, 2, 3, 3, 2],
    "Team Gamma": [2, 3, 3, 2, 1, 3],
    "Team Delta": [4, 4, 5, 4, 4, 4],
    "Team Epsilon": [5, 5, 4, 5, 5, 5],
}

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#2ecc71", "#e74c3c", "#9b59b6"]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

x = np.arange(len(periods))

for i, (entity, ranks) in enumerate(rankings.items()):
    ax.plot(x, ranks, marker="o", markersize=15, linewidth=3, color=colors[i], label=entity)

# Invert Y-axis so rank 1 is at top
ax.invert_yaxis()

# Labels and styling
ax.set_xlabel("Period", fontsize=20)
ax.set_ylabel("Rank", fontsize=20)
ax.set_title("bump-basic · matplotlib · pyplots.ai", fontsize=24)

ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.set_yticks(range(1, len(entities) + 1))
ax.tick_params(axis="both", labelsize=16)

ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=16, loc="upper left", bbox_to_anchor=(1.02, 1))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
