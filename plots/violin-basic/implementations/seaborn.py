"""pyplots.ai
violin-basic: Basic Violin Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Salary distributions across departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = []

for cat in categories:
    # Different distribution shapes per category
    if cat == "Engineering":
        values = np.random.normal(85000, 15000, 150)
    elif cat == "Marketing":
        values = np.random.normal(70000, 12000, 150)
    elif cat == "Sales":
        # Bimodal distribution for sales (junior vs senior)
        values = np.concatenate([np.random.normal(55000, 8000, 75), np.random.normal(90000, 10000, 75)])
    else:  # Support
        values = np.random.normal(55000, 10000, 150)

    for v in values:
        data.append({"Department": cat, "Salary": v})

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.violinplot(
    data=df,
    x="Department",
    y="Salary",
    hue="Department",
    palette=["#306998", "#FFD43B", "#306998", "#FFD43B"],
    inner="quart",  # Show quartiles inside violin
    linewidth=2,
    legend=False,
    ax=ax,
)

# Style
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Salary ($)", fontsize=20)
ax.set_title("violin-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}k"))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
