""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
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
species_names = ["Setosa", "Versicolor", "Virginica"]

# Select 10 samples from each species (30 total) for clearer visualization
indices = np.concatenate([np.random.choice(np.where(iris.target == i)[0], 10, replace=False) for i in range(3)])

X = iris.data[indices]

# Create clear labels: Species-Number format using vectorized approach
species_ids = iris.target[indices]
labels = [f"{species_names[sid]}-{np.sum(species_ids[: i + 1] == sid)}" for i, sid in enumerate(species_ids)]

# Compute linkage matrix using Ward's method
linkage_matrix = linkage(X, method="ward")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Define custom colors using seaborn colorblind palette for species
palette = sns.color_palette("colorblind", n_colors=3)
species_color_map = dict(zip(species_names, palette, strict=True))

# Create dendrogram
dendrogram(
    linkage_matrix,
    labels=labels,
    leaf_rotation=45,
    leaf_font_size=14,
    ax=ax,
    above_threshold_color="#888888",
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
)

# Color the x-axis labels by species using exact palette colors
for lbl in ax.get_xticklabels():
    text = lbl.get_text()
    species = text.rsplit("-", 1)[0]
    if species in species_color_map:
        lbl.set_color(species_color_map[species])
        lbl.set_fontweight("bold")

# Style the plot with seaborn-compatible settings
ax.set_xlabel("Iris Samples (by Species)", fontsize=20)
ax.set_ylabel("Distance (Ward Linkage)", fontsize=20)
ax.set_title("dendrogram-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="y", labelsize=16)
ax.tick_params(axis="x", labelsize=14)

# Make grid subtle
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Add legend using scatter plot handles for exact color matching
for i, species in enumerate(species_names):
    ax.scatter([], [], c=[palette[i]], s=150, label=species, marker="s")
ax.legend(title="Species", loc="upper right", fontsize=14, title_fontsize=16, framealpha=0.9)

# Remove top and right spines for cleaner look
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
