"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Product quality scores across manufacturing lines
np.random.seed(42)

categories = ["Line A", "Line B", "Line C", "Line D", "Line E"]
n_per_category = 25

data = []
for cat in categories:
    if cat == "Line A":
        values = np.random.normal(85, 5, n_per_category)
    elif cat == "Line B":
        values = np.random.normal(78, 8, n_per_category)
    elif cat == "Line C":
        values = np.random.normal(92, 3, n_per_category)
    elif cat == "Line D":
        values = np.random.normal(75, 10, n_per_category)
    else:
        values = np.random.normal(88, 6, n_per_category)

    for v in values:
        data.append({"Manufacturing Line": cat, "Quality Score": v})

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.stripplot(
    data=df,
    x="Manufacturing Line",
    y="Quality Score",
    hue="Manufacturing Line",
    palette=["#306998", "#FFD43B", "#4B8BBE", "#646464", "#F0DB4F"],
    size=12,
    jitter=0.25,
    alpha=0.8,
    ax=ax,
    legend=False,
)

# Style
ax.set_title("cat-strip · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.set_xlabel("Manufacturing Line", fontsize=20)
ax.set_ylabel("Quality Score", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Set y-axis range to show full data
ax.set_ylim(45, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
