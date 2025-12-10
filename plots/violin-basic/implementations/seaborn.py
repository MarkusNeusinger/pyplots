"""
violin-basic: Basic Violin Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Employee performance scores grouped by department
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "Support", "Design"]
data = []

for dept in departments:
    n = np.random.randint(80, 150)
    if dept == "Engineering":
        scores = np.random.normal(75, 12, n)
    elif dept == "Marketing":
        scores = np.concatenate([np.random.normal(65, 8, n // 2), np.random.normal(85, 6, n // 2)])
    elif dept == "Sales":
        scores = np.random.normal(70, 15, n)
    elif dept == "Support":
        scores = np.random.normal(72, 10, n)
    else:  # Design
        scores = np.random.normal(80, 8, n)
    scores = np.clip(scores, 0, 100)
    for score in scores:
        data.append({"Department": dept, "Performance Score": score})

df = pd.DataFrame(data)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Violin plot with inner box plot markers
sns.violinplot(
    data=df,
    x="Department",
    y="Performance Score",
    hue="Department",
    palette=colors,
    inner="box",
    linewidth=1.5,
    saturation=0.9,
    legend=False,
    ax=ax,
)

# Styling
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Performance Score", fontsize=20)
ax.set_title("Employee Performance Score Distribution by Department", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="-")
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
