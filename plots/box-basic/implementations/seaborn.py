""" pyplots.ai
box-basic: Basic Box Plot
Library: seaborn 0.13.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
data = []

for category in categories:
    if category == "Engineering":
        values = np.random.normal(95000, 15000, 80)
    elif category == "Marketing":
        values = np.random.normal(75000, 12000, 60)
    elif category == "Sales":
        values = np.random.normal(70000, 20000, 100)
    elif category == "HR":
        values = np.random.normal(65000, 10000, 50)
    else:  # Finance
        values = np.random.normal(85000, 18000, 70)

    outliers = np.random.uniform(values.min() - 20000, values.max() + 25000, 3)
    values = np.concatenate([values, outliers])

    for v in values:
        data.append({"Department": category, "Salary": v})

df = pd.DataFrame(data)

# Plot
palette = ["#306998", "#E8A838", "#4CAF50", "#FF7043", "#9C27B0"]

fig, ax = plt.subplots(figsize=(16, 9))

sns.boxplot(
    data=df,
    x="Department",
    y="Salary",
    hue="Department",
    palette=palette,
    linewidth=2.5,
    fliersize=0,
    width=0.6,
    legend=False,
    ax=ax,
)

sns.stripplot(
    data=df,
    x="Department",
    y="Salary",
    hue="Department",
    palette=palette,
    size=4,
    alpha=0.35,
    jitter=0.25,
    legend=False,
    ax=ax,
)

# Style
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Salary ($)", fontsize=20)
ax.set_title("box-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}K"))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
