"""pyplots.ai
scatter-text: Scatter Plot with Text Labels Instead of Points
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Data - Programming language names with 2D coordinates (simulating dimensionality reduction)
np.random.seed(42)

languages = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "Ruby",
    "Go",
    "Rust",
    "Swift",
    "Kotlin",
    "TypeScript",
    "PHP",
    "Scala",
    "R",
    "Julia",
    "Perl",
    "Haskell",
    "Elixir",
    "Clojure",
    "F#",
    "Dart",
    "Lua",
    "MATLAB",
    "SQL",
    "Bash",
]

# Generate coordinates that show some clustering (like a t-SNE output)
x = np.concatenate(
    [
        np.random.normal(-3, 1.2, 6),  # Systems languages cluster
        np.random.normal(0, 1.0, 8),  # General-purpose cluster
        np.random.normal(3, 1.0, 6),  # Scripting languages cluster
        np.random.normal(1, 1.5, 4),  # Functional languages
    ]
)
y = np.concatenate(
    [
        np.random.normal(2, 1.0, 6),  # High performance
        np.random.normal(0, 1.2, 8),  # Balanced
        np.random.normal(-2, 1.0, 6),  # Easy to learn
        np.random.normal(3, 0.8, 4),  # Academic/niche
    ]
)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create a scatter plot for the underlying structure (invisible points)
# This allows seaborn to set up axes properly
sns.scatterplot(x=x, y=y, ax=ax, alpha=0, legend=False)

# Add text labels at each coordinate position
colors = [
    "#306998",
    "#FFD43B",
    "#3C873A",
    "#00599C",
    "#CC342D",
    "#00ADD8",
    "#DEA584",
    "#FA7343",
    "#B125EA",
    "#3178C6",
    "#777BB4",
    "#DC322F",
    "#276DC3",
    "#9558B2",
    "#39457E",
    "#5D4F85",
    "#6E4A7E",
    "#63B132",
    "#378BBA",
    "#00B4AB",
    "#000080",
    "#FF6F00",
    "#336791",
    "#4EAA25",
]

for i, (xi, yi, label) in enumerate(zip(x, y, languages, strict=True)):
    color = colors[i % len(colors)]
    ax.text(xi, yi, label, fontsize=16, fontweight="bold", ha="center", va="center", color=color, alpha=0.85)

# Styling
ax.set_xlabel("Dimension 1 (t-SNE)", fontsize=20)
ax.set_ylabel("Dimension 2 (t-SNE)", fontsize=20)
ax.set_title("scatter-text · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Adjust axis limits to give text some padding
x_margin = (x.max() - x.min()) * 0.15
y_margin = (y.max() - y.min()) * 0.15
ax.set_xlim(x.min() - x_margin, x.max() + x_margin)
ax.set_ylim(y.min() - y_margin, y.max() + y_margin)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
