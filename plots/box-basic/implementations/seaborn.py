""" pyplots.ai
box-basic: Basic Box Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-14
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
    # Generate realistic salary distributions with different characteristics
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

    # Add some outliers
    outliers = np.random.uniform(values.min() - 20000, values.max() + 25000, 3)
    values = np.concatenate([values, outliers])

    for v in values:
        data.append({"Department": category, "Salary": v})

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Use hue with palette to avoid seaborn 0.14+ warning
sns.boxplot(
    data=df,
    x="Department",
    y="Salary",
    hue="Department",
    palette=["#306998", "#FFD43B", "#4CAF50", "#FF7043", "#9C27B0"],
    linewidth=2.5,
    fliersize=10,
    width=0.6,
    legend=False,
    ax=ax,
)

# Style
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Salary ($)", fontsize=20)
ax.set_title("box-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}K"))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
