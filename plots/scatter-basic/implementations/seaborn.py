""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: seaborn 0.13.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Data - Palmer penguins: bill length vs body mass by species
penguins = sns.load_dataset("penguins").dropna(subset=["bill_length_mm", "body_mass_g"])

# Create plot
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(16, 9))
sns.scatterplot(
    data=penguins,
    x="bill_length_mm",
    y="body_mass_g",
    hue="species",
    style="species",
    palette="colorblind",
    s=80,
    alpha=0.7,
    edgecolor="white",
    linewidth=0.5,
    ax=ax,
)

# Labels and styling
ax.set_xlabel("Bill Length (mm)", fontsize=20)
ax.set_ylabel("Body Mass (g)", fontsize=20)
ax.set_title("Palmer Penguins · scatter-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.25, linestyle="--")

# Legend styling
ax.legend(title="Species", fontsize=16, title_fontsize=18, markerscale=1.5, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
