""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Simulate product quality scores across manufacturing plants
np.random.seed(42)

categories = ["Plant A", "Plant B", "Plant C", "Plant D", "Plant E"]
n_per_category = 25

data = {"Plant": [], "Quality Score": []}

# Create different distributions for each plant to show variety
distributions = [
    (85, 5),  # Plant A: high quality, consistent
    (75, 10),  # Plant B: medium quality, variable
    (90, 3),  # Plant C: excellent quality, very consistent
    (70, 15),  # Plant D: lower quality, high variability
    (82, 8),  # Plant E: good quality, moderate variability
]

for cat, (mean, std) in zip(categories, distributions, strict=True):
    values = np.random.normal(mean, std, n_per_category)
    values = np.clip(values, 40, 100)  # Clip to realistic range
    data["Plant"].extend([cat] * n_per_category)
    data["Quality Score"].extend(values)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.stripplot(
    x="Plant",
    y="Quality Score",
    data=data,
    hue="Plant",
    palette=["#306998", "#FFD43B", "#4B8BBE", "#646464", "#B07219"],
    size=12,
    alpha=0.7,
    jitter=0.3,
    legend=False,
    ax=ax,
)

# Styling
ax.set_xlabel("Manufacturing Plant", fontsize=20)
ax.set_ylabel("Quality Score (%)", fontsize=20)
ax.set_title("cat-strip · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Set y-axis range
ax.set_ylim(35, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
