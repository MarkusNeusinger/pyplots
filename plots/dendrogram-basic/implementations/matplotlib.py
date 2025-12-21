""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage


# Data - Iris flower measurements (4 features for 15 samples)
np.random.seed(42)

# Simulate iris-like measurements: sepal length, sepal width, petal length, petal width
# Three species with distinct characteristics
samples_per_species = 5

labels = []
data = []

# Setosa: shorter petals, wider sepals
for i in range(samples_per_species):
    labels.append(f"Setosa-{i + 1}")
    data.append(
        [
            5.0 + np.random.randn() * 0.3,  # sepal length
            3.4 + np.random.randn() * 0.3,  # sepal width
            1.5 + np.random.randn() * 0.2,  # petal length
            0.3 + np.random.randn() * 0.1,  # petal width
        ]
    )

# Versicolor: medium measurements
for i in range(samples_per_species):
    labels.append(f"Versicolor-{i + 1}")
    data.append(
        [
            5.9 + np.random.randn() * 0.4,  # sepal length
            2.8 + np.random.randn() * 0.3,  # sepal width
            4.3 + np.random.randn() * 0.4,  # petal length
            1.3 + np.random.randn() * 0.2,  # petal width
        ]
    )

# Virginica: longer petals and sepals
for i in range(samples_per_species):
    labels.append(f"Virginica-{i + 1}")
    data.append(
        [
            6.6 + np.random.randn() * 0.5,  # sepal length
            3.0 + np.random.randn() * 0.3,  # sepal width
            5.5 + np.random.randn() * 0.5,  # petal length
            2.0 + np.random.randn() * 0.3,  # petal width
        ]
    )

data = np.array(data)

# Compute hierarchical clustering using Ward's method
linkage_matrix = linkage(data, method="ward")

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Create dendrogram with custom colors
dendrogram(
    linkage_matrix,
    labels=labels,
    ax=ax,
    leaf_rotation=45,
    leaf_font_size=14,
    above_threshold_color="#306998",  # Python Blue for main branches
    color_threshold=0.7 * max(linkage_matrix[:, 2]),  # Color threshold for clusters
)

# Style
ax.set_xlabel("Sample", fontsize=20)
ax.set_ylabel("Distance (Ward)", fontsize=20)
ax.set_title("dendrogram-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="x", labelsize=14, rotation=45)

# Adjust spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add subtle grid on y-axis only
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
