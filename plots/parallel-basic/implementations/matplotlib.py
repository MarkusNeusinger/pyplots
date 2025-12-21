""" pyplots.ai
parallel-basic: Basic Parallel Coordinates Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data - Iris dataset for multivariate demonstration
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

# Define numeric columns and normalize to [0, 1] for fair comparison
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
df_norm = df.copy()
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    df_norm[col] = (df[col] - min_val) / (max_val - min_val)

# Create figure (4800x2700 px at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors for species
colors = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#4CAF50"}

# Plot parallel coordinates - each line connects values across axes
x = range(len(numeric_cols))
for _, row in df_norm.iterrows():
    y = [row[col] for col in numeric_cols]
    ax.plot(x, y, color=colors[row["species"]], alpha=0.5, linewidth=2)

# Axis labels with original scale ranges
ax.set_xticks(x)
labels = [
    f"Sepal Length\n({df['sepal_length'].min():.1f}-{df['sepal_length'].max():.1f} cm)",
    f"Sepal Width\n({df['sepal_width'].min():.1f}-{df['sepal_width'].max():.1f} cm)",
    f"Petal Length\n({df['petal_length'].min():.1f}-{df['petal_length'].max():.1f} cm)",
    f"Petal Width\n({df['petal_width'].min():.1f}-{df['petal_width'].max():.1f} cm)",
]
ax.set_xticklabels(labels, fontsize=18)
ax.set_ylabel("Normalized Value", fontsize=20)
ax.set_title("parallel-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="y", labelsize=16)

# Add legend for species
legend_handles = [
    plt.Line2D([0], [0], color=colors["setosa"], linewidth=3, label="Setosa"),
    plt.Line2D([0], [0], color=colors["versicolor"], linewidth=3, label="Versicolor"),
    plt.Line2D([0], [0], color=colors["virginica"], linewidth=3, label="Virginica"),
]
ax.legend(handles=legend_handles, fontsize=16, loc="upper right")

# Styling
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
