"""
dendrogram-basic: Basic Dendrogram
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage


# Data - Iris-like flower measurements for 15 samples
np.random.seed(42)

# Create realistic flower measurement data (sepal length, sepal width, petal length, petal width)
# Three species with distinct characteristics
species_names = ["Setosa", "Versicolor", "Virginica"]
samples_per_species = 5

# Setosa: small petals, wide sepals
setosa = np.random.randn(samples_per_species, 4) * 0.3 + [5.0, 3.4, 1.5, 0.2]
# Versicolor: medium measurements
versicolor = np.random.randn(samples_per_species, 4) * 0.4 + [5.9, 2.8, 4.3, 1.3]
# Virginica: large petals
virginica = np.random.randn(samples_per_species, 4) * 0.4 + [6.6, 3.0, 5.5, 2.0]

data = np.vstack([setosa, versicolor, virginica])
labels = [f"{species_names[i // samples_per_species]} {i % samples_per_species + 1}" for i in range(15)]

# Compute hierarchical clustering
linkage_matrix = linkage(data, method="ward")

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

dendrogram(
    linkage_matrix,
    labels=labels,
    ax=ax,
    leaf_rotation=45,
    leaf_font_size=14,
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
    above_threshold_color="#306998",
)

# Style
ax.set_xlabel("Sample", fontsize=20)
ax.set_ylabel("Distance (Ward)", fontsize=20)
ax.set_title("dendrogram-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
