"""
scatter-color-groups: Scatter Plot with Color Groups
Library: seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Data - use iris dataset as specified in the spec
data = sns.load_dataset("iris")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot - scatter with color by species (group)
sns.scatterplot(
    data=data,
    x="sepal_length",
    y="sepal_width",
    hue="species",
    palette=["#306998", "#FFD43B", "#DC2626"],
    s=100,
    alpha=0.7,
    ax=ax,
)

# Labels and styling
ax.set_xlabel("Sepal Length (cm)", fontsize=20)
ax.set_ylabel("Sepal Width (cm)", fontsize=20)
ax.set_title("Iris Species by Sepal Dimensions", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3)

# Legend styling
ax.legend(title="Species", fontsize=16, title_fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
