"""
scatter-color-groups: Scatter Plot with Color Groups
Library: matplotlib
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Data
data = sns.load_dataset("iris")

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
