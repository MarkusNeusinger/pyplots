"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Survey responses about preferred programming languages
np.random.seed(42)
languages = ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"]
# Weighted probabilities to create realistic distribution (Python most popular)
weights = [0.28, 0.22, 0.15, 0.12, 0.10, 0.07, 0.06]
responses = np.random.choice(languages, size=500, p=weights)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn countplot for automatic frequency counting
sns.countplot(
    x=responses,
    order=["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
    hue=responses,
    hue_order=["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
    palette=["#306998", "#FFD43B", "#5382A1", "#00599C", "#00ADD8", "#DEA584", "#3178C6"],
    legend=False,
    ax=ax,
)

# Add count labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fontsize=16, padding=5)

# Styling
ax.set_xlabel("Programming Language", fontsize=20)
ax.set_ylabel("Number of Responses", fontsize=20)
ax.set_title("bar-categorical · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(axis="y", alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
