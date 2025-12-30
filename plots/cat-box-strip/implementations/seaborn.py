"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Four product categories with different distributions
np.random.seed(42)

categories = ["Product A", "Product B", "Product C", "Product D"]
n_per_group = 40

data = {"Category": [], "Customer Rating": []}

# Product A: high ratings, tight distribution
ratings_a = np.random.normal(loc=4.2, scale=0.3, size=n_per_group)
ratings_a = np.clip(ratings_a, 1, 5)

# Product B: moderate ratings, wider distribution
ratings_b = np.random.normal(loc=3.5, scale=0.6, size=n_per_group)
ratings_b = np.clip(ratings_b, 1, 5)

# Product C: lower ratings with some outliers
ratings_c = np.random.normal(loc=2.8, scale=0.5, size=n_per_group)
ratings_c = np.clip(ratings_c, 1, 5)
ratings_c[0] = 4.8  # Add an outlier

# Product D: bimodal-like, varied distribution
ratings_d = np.concatenate(
    [
        np.random.normal(loc=3.0, scale=0.4, size=n_per_group // 2),
        np.random.normal(loc=4.0, scale=0.3, size=n_per_group // 2),
    ]
)
ratings_d = np.clip(ratings_d, 1, 5)

for cat, ratings in zip(categories, [ratings_a, ratings_b, ratings_c, ratings_d], strict=True):
    data["Category"].extend([cat] * len(ratings))
    data["Customer Rating"].extend(ratings)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Box plot (light colors, no fliers since strip shows all points)
sns.boxplot(
    data=data,
    x="Category",
    y="Customer Rating",
    hue="Category",
    palette=["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B"],
    width=0.5,
    linewidth=2.5,
    fliersize=0,
    legend=False,
    ax=ax,
)

# Strip plot overlay (darker for visibility)
sns.stripplot(
    data=data,
    x="Category",
    y="Customer Rating",
    hue="Category",
    palette=["#1e4260", "#c9a82c", "#3aa89a", "#cc5555"],
    size=10,
    alpha=0.7,
    jitter=0.15,
    legend=False,
    ax=ax,
)

# Styling
ax.set_title("cat-box-strip · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.set_xlabel("Category", fontsize=20)
ax.set_ylabel("Customer Rating (1-5)", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0.5, 5.5)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Clean spine styling
sns.despine(left=False, bottom=False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
