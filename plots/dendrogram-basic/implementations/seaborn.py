"""pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: seaborn 0.13.2 | Python 3.14.3
Quality: /100 | Updated: 2026-04-05
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, set_link_color_palette


# Style
sns.set_theme(style="white", rc={"axes.linewidth": 0.8})
sns.set_context("talk", font_scale=1.2)
palette = sns.color_palette("colorblind", n_colors=3)

# Data - use seaborn's iris dataset (30 samples for readable dendrogram)
np.random.seed(42)
iris = sns.load_dataset("iris")
species_names = ["setosa", "versicolor", "virginica"]
display_names = ["Setosa", "Versicolor", "Virginica"]
species_color = dict(zip(display_names, palette, strict=True))

samples = (
    iris.groupby("species").apply(lambda g: g.sample(10, random_state=42), include_groups=False).reset_index(level=0)
)

features = samples[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values

# Build labels: Species-Number
counters = dict.fromkeys(species_names, 0)
labels = []
for species in samples["species"]:
    counters[species] += 1
    labels.append(f"{species.title()}-{counters[species]}")

# Compute linkage
linkage_matrix = linkage(features, method="ward")

# Map dendrogram branch colors to species palette
hex_colors = ["#{:02x}{:02x}{:02x}".format(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)) for c in palette]
set_link_color_palette(hex_colors)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

dendrogram(
    linkage_matrix,
    labels=labels,
    leaf_rotation=45,
    leaf_font_size=14,
    ax=ax,
    above_threshold_color="#aaaaaa",
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
)

set_link_color_palette(None)

# Color x-axis labels by species
for lbl in ax.get_xticklabels():
    species = lbl.get_text().rsplit("-", 1)[0]
    if species in species_color:
        lbl.set_color(species_color[species])
        lbl.set_fontweight("bold")

# Axes and title
ax.set_xlabel("Iris Samples (by Species)", fontsize=20)
ax.set_ylabel("Distance (Ward Linkage)", fontsize=20)
ax.set_title("dendrogram-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="y", labelsize=16)
ax.tick_params(axis="x", labelsize=14)

# Grid and spines
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8, color="#cccccc")
ax.set_axisbelow(True)
sns.despine(ax=ax)

# Legend
for name, color in species_color.items():
    ax.scatter([], [], c=[color], s=150, label=name, marker="s")
ax.legend(title="Species", loc="upper right", fontsize=14, title_fontsize=16, framealpha=0.9, edgecolor="#dddddd")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
