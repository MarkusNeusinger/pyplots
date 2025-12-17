"""
dendrogram-basic: Basic Dendrogram
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")

# Data: Iris-like measurements for different flower samples
np.random.seed(42)

# Create sample data representing flower measurements
# 15 samples with 4 features each (sepal/petal length/width)
labels = [
    "Setosa A",
    "Setosa B",
    "Setosa C",
    "Setosa D",
    "Setosa E",
    "Versicolor A",
    "Versicolor B",
    "Versicolor C",
    "Versicolor D",
    "Versicolor E",
    "Virginica A",
    "Virginica B",
    "Virginica C",
    "Virginica D",
    "Virginica E",
]

# Generate clustered data - each species has similar characteristics
setosa_data = np.random.randn(5, 4) * 0.3 + np.array([5.0, 3.4, 1.5, 0.2])
versicolor_data = np.random.randn(5, 4) * 0.4 + np.array([5.9, 2.8, 4.3, 1.3])
virginica_data = np.random.randn(5, 4) * 0.5 + np.array([6.6, 3.0, 5.5, 2.0])

data = np.vstack([setosa_data, versicolor_data, virginica_data])

# Compute hierarchical clustering using Ward's method
linkage_matrix = linkage(data, method="ward")

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Create dendrogram
dendrogram(
    linkage_matrix,
    labels=labels,
    ax=ax,
    leaf_rotation=45,
    leaf_font_size=14,
    above_threshold_color="#306998",
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
)

# Style
ax.set_xlabel("Flower Samples", fontsize=20)
ax.set_ylabel("Distance (Ward)", fontsize=20)
ax.set_title("dendrogram-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="x", labelsize=14, rotation=45)

# Adjust grid to be subtle
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Remove top and right spines for cleaner look
sns.despine()

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
