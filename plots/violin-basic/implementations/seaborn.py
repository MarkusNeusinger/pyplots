""" pyplots.ai
violin-basic: Basic Violin Plot
Library: seaborn 0.13.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Salary distributions across departments
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "Support"]
records = []

for dept in departments:
    if dept == "Engineering":
        salaries = np.random.normal(85000, 15000, 150)
    elif dept == "Marketing":
        salaries = np.random.normal(70000, 12000, 150)
    elif dept == "Sales":
        # Bimodal distribution (junior vs senior) — showcases KDE strength
        salaries = np.concatenate([np.random.normal(55000, 8000, 75), np.random.normal(90000, 10000, 75)])
    else:
        salaries = np.random.normal(55000, 10000, 150)
    for s in salaries:
        records.append({"Department": dept, "Salary": s})

df = pd.DataFrame(records)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.violinplot(
    data=df,
    x="Department",
    y="Salary",
    hue="Department",
    palette=["#306998", "#4A90C4", "#2D5F8A", "#5BA3D9"],
    inner="box",
    cut=0,
    linewidth=1.5,
    saturation=0.9,
    legend=False,
    ax=ax,
)

# Style
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Salary ($)", fontsize=20)
ax.set_title("violin-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}k"))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
