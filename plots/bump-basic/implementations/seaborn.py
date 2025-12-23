""" pyplots.ai
bump-basic: Basic Bump Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - Sports league standings over 6 weeks
data = {
    "Team": ["Lions"] * 6 + ["Tigers"] * 6 + ["Bears"] * 6 + ["Eagles"] * 6 + ["Wolves"] * 6,
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"] * 5,
    "Rank": [
        3,
        2,
        1,
        1,
        2,
        1,  # Lions - start mid, climb to top
        1,
        1,
        2,
        3,
        1,
        2,  # Tigers - start top, fluctuate
        5,
        4,
        4,
        2,
        3,
        3,  # Bears - steady climb from bottom
        2,
        3,
        3,
        4,
        4,
        5,  # Eagles - gradual decline
        4,
        5,
        5,
        5,
        5,
        4,  # Wolves - mostly bottom, slight recovery
    ],
}
df = pd.DataFrame(data)

# Colors for each team - Python Blue first, then distinct colorblind-safe colors
palette = ["#306998", "#FFD43B", "#E74C3C", "#2ECC71", "#9B59B6"]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.lineplot(data=df, x="Week", y="Rank", hue="Team", marker="o", markersize=18, linewidth=4, palette=palette, ax=ax)

# Invert y-axis so rank 1 is at top
ax.invert_yaxis()

# Set y-axis ticks to integer ranks only
ax.set_yticks([1, 2, 3, 4, 5])

# Styling
ax.set_xlabel("Week", fontsize=20)
ax.set_ylabel("Rank", fontsize=20)
ax.set_title("bump-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Legend styling - placed outside plot area
ax.legend(title="Team", fontsize=14, title_fontsize=16, loc="center left", bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
