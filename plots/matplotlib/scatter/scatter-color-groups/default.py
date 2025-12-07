"""
scatter-color-groups: Scatter Plot with Color Groups
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Iris-like dataset
np.random.seed(42)
n_per_group = 50

data = pd.DataFrame(
    {
        "sepal_length": np.concatenate(
            [
                np.random.normal(5.0, 0.35, n_per_group),
                np.random.normal(5.9, 0.50, n_per_group),
                np.random.normal(6.6, 0.60, n_per_group),
            ]
        ),
        "sepal_width": np.concatenate(
            [
                np.random.normal(3.4, 0.38, n_per_group),
                np.random.normal(2.8, 0.30, n_per_group),
                np.random.normal(3.0, 0.30, n_per_group),
            ]
        ),
        "species": ["setosa"] * n_per_group + ["versicolor"] * n_per_group + ["virginica"] * n_per_group,
    }
)

# Color palette (colorblind safe from style guide)
colors = ["#306998", "#FFD43B", "#DC2626"]
species = data["species"].unique()
color_map = {sp: colors[i] for i, sp in enumerate(species)}

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

for species_name in species:
    subset = data[data["species"] == species_name]
    ax.scatter(
        subset["sepal_length"],
        subset["sepal_width"],
        c=color_map[species_name],
        label=species_name.capitalize(),
        alpha=0.7,
        s=80,
        edgecolors="white",
        linewidths=0.5,
    )

# Labels and styling
ax.set_xlabel("Sepal Length (cm)", fontsize=20)
ax.set_ylabel("Sepal Width (cm)", fontsize=20)
ax.set_title("Iris Species by Sepal Dimensions", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.legend(title="Species", fontsize=16, title_fontsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
