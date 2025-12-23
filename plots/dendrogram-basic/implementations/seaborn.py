""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import load_iris


# Set seaborn style for better aesthetics
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Load iris dataset - use subset for readability (spec recommends 10-50 items)
np.random.seed(42)
iris = load_iris()

# Select 10 samples from each species (30 total) for clearer visualization
indices = np.concatenate([np.random.choice(np.where(iris.target == i)[0], 10, replace=False) for i in range(3)])
X = iris.data[indices]
labels = [f"{iris.target_names[iris.target[i]][:4].title()} {j + 1}" for j, i in enumerate(indices)]

# Compute linkage matrix using Ward's method
linkage_matrix = linkage(X, method="ward")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Define custom colors using seaborn colorblind palette
palette = sns.color_palette("colorblind", n_colors=3)

# Create dendrogram with scipy's built-in coloring
dend = dendrogram(
    linkage_matrix,
    labels=labels,
    leaf_rotation=45,
    leaf_font_size=12,
    ax=ax,
    above_threshold_color="#888888",
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
)

# Style the plot with seaborn-compatible settings
ax.set_xlabel("Iris Sample", fontsize=20)
ax.set_ylabel("Distance (Ward Linkage)", fontsize=20)
ax.set_title("dendrogram-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="y", labelsize=16)
ax.tick_params(axis="x", labelsize=14)

# Make grid subtle
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Remove top and right spines for cleaner look
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
