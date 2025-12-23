""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch
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
indices = []
for i in range(3):
    species_indices = np.where(iris.target == i)[0]
    selected = np.random.choice(species_indices, 10, replace=False)
    indices.extend(selected)
indices = np.array(indices)

X = iris.data[indices]

# Create clear labels: Species-Number format
labels = []
species_count = {0: 0, 1: 0, 2: 0}
for idx in indices:
    species_id = iris.target[idx]
    species_count[species_id] += 1
    labels.append(f"{species_names[species_id]}-{species_count[species_id]}")

# Compute linkage matrix using Ward's method
linkage_matrix = linkage(X, method="ward")

# Create figure
_, ax = plt.subplots(figsize=(16, 9))

# Define custom colors using seaborn colorblind palette for species
palette = sns.color_palette("colorblind", n_colors=3)
species_colors = {species_names[i]: palette[i] for i in range(3)}

# Map each leaf label to its species color
label_colors = {}
for label in labels:
    species = label.rsplit("-", 1)[0]
    label_colors[label] = species_colors[species]

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

# Color the x-axis labels by species
x_labels = ax.get_xticklabels()
for lbl in x_labels:
    text = lbl.get_text()
    if text in label_colors:
        lbl.set_color(label_colors[text])
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

# Add legend explaining species colors
legend_elements = [Patch(facecolor=palette[i], label=species_names[i]) for i in range(3)]
ax.legend(handles=legend_elements, title="Species", loc="upper right", fontsize=14, title_fontsize=16)

# Remove top and right spines for cleaner look
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
