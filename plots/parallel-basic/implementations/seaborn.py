"""
parallel-basic: Basic Parallel Coordinates Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Iris dataset as recommended in the specification
iris = sns.load_dataset("iris")

# Prepare data: normalize numeric columns to 0-1 scale (manual min-max scaling)
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
iris_scaled = iris.copy()
for col in numeric_cols:
    col_min = iris[col].min()
    col_max = iris[col].max()
    iris_scaled[col] = (iris[col] - col_min) / (col_max - col_min)

# Create figure (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors for each species using Python Blue and Yellow plus a third
palette = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#4ECDC4"}

# Create parallel coordinates plot
x_coords = np.arange(len(numeric_cols))

# Plot each observation as a line connecting values across axes
for species in iris_scaled["species"].unique():
    subset = iris_scaled[iris_scaled["species"] == species]
    for _idx, row in subset.iterrows():
        values = [row[col] for col in numeric_cols]
        ax.plot(x_coords, values, color=palette[species], alpha=0.4, linewidth=2)

# Add legend handles
for species, color in palette.items():
    ax.plot([], [], color=color, linewidth=3, label=species.capitalize(), alpha=0.8)

# Style the axes
ax.set_xticks(x_coords)
ax.set_xticklabels(["Sepal\nLength", "Sepal\nWidth", "Petal\nLength", "Petal\nWidth"], fontsize=18)
ax.tick_params(axis="y", labelsize=16)

# Add vertical lines at each axis
for x in x_coords:
    ax.axvline(x=x, color="gray", linestyle="-", linewidth=1, alpha=0.5)

# Labels and title
ax.set_ylabel("Normalized Value", fontsize=20)
ax.set_title("parallel-basic · seaborn · pyplots.ai", fontsize=24)
ax.set_ylim(-0.05, 1.05)
ax.set_xlim(-0.2, len(numeric_cols) - 0.8)

# Legend
ax.legend(fontsize=16, loc="upper right", framealpha=0.9)

# Grid
ax.grid(True, axis="y", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
