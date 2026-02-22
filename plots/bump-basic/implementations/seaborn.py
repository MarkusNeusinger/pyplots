"""pyplots.ai
bump-basic: Basic Bump Chart
Library: seaborn 0.13.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-22
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - Sports league standings over 6 weeks
teams = ["Lions", "Tigers", "Bears", "Eagles", "Wolves"]
weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]
ranks = [
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
]
df = pd.DataFrame(
    {"Team": [team for team in teams for _ in weeks], "Competition Week": weeks * len(teams), "League Position": ranks}
)

# Palette - Python Blue first, then distinct colorblind-safe colors
palette = ["#306998", "#FFD43B", "#E74C3C", "#2ECC71", "#9B59B6"]

# Plot
sns.set_theme(
    style="whitegrid",
    rc={"axes.spines.top": False, "axes.spines.right": False, "grid.linestyle": "--", "grid.alpha": 0.2},
)
fig, ax = plt.subplots(figsize=(16, 9))

sns.lineplot(
    data=df,
    x="Competition Week",
    y="League Position",
    hue="Team",
    style="Team",
    markers=True,
    dashes=False,
    markersize=18,
    linewidth=4,
    palette=palette,
    sort=False,
    ax=ax,
)

# Invert y-axis so rank 1 is at top
ax.invert_yaxis()
ax.set_yticks([1, 2, 3, 4, 5])
ax.xaxis.grid(False)

# Style
ax.set_xlabel("Competition Week", fontsize=20)
ax.set_ylabel("League Position", fontsize=20)
ax.set_title("bump-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

# Legend
ax.legend(title="Team", fontsize=14, title_fontsize=16, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
