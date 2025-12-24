"""pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set random seed for reproducibility
np.random.seed(42)

# Data - Tech industry survey responses about skills
word_frequencies = {
    "Python": 150,
    "JavaScript": 120,
    "DataScience": 110,
    "ML": 100,
    "Cloud": 95,
    "API": 90,
    "Database": 85,
    "Security": 80,
    "DevOps": 75,
    "Docker": 70,
    "Kubernetes": 65,
    "React": 60,
    "SQL": 58,
    "AWS": 55,
    "Git": 52,
    "Agile": 50,
    "Testing": 48,
    "Linux": 45,
    "TypeScript": 42,
    "Node": 40,
    "REST": 38,
    "CI/CD": 35,
    "Azure": 30,
    "MongoDB": 28,
    "Redis": 26,
    "GraphQL": 24,
    "Terraform": 22,
    "Spark": 20,
    "Analytics": 18,
    "Backend": 16,
}

# Convert to DataFrame for seaborn
words = list(word_frequencies.keys())
frequencies = list(word_frequencies.values())
n_words = len(words)

# Sort by frequency descending
sorted_pairs = sorted(zip(words, frequencies, strict=True), key=lambda x: -x[1])
words = [p[0] for p in sorted_pairs]
frequencies = [p[1] for p in sorted_pairs]

# Grid-based layout with variable row heights
n_cols = 5
x_positions = []
y_positions = []

x_base = 3.6
y_levels = [0.9, 0.5, 0.15, -0.15, -0.45, -0.75]

row = 0
col = 0
for _i in range(n_words):
    x_offset = (np.random.random() - 0.5) * 0.15
    y_offset = (np.random.random() - 0.5) * 0.08
    x_pos = (col - n_cols / 2 + 0.5) * (x_base / n_cols) + x_offset
    y_pos = y_levels[min(row, len(y_levels) - 1)] + y_offset
    x_positions.append(x_pos)
    y_positions.append(y_pos)
    col += 1
    if col >= n_cols:
        col = 0
        row += 1

# Normalize frequencies for marker sizing
freq_array = np.array(frequencies)
size_normalized = (freq_array / freq_array.max()) * 2000 + 400

# Create DataFrame
df = pd.DataFrame(
    {"word": words, "frequency": frequencies, "x": x_positions, "y": y_positions, "size": size_normalized}
)

# Plot using seaborn
sns.set_theme(style="white", context="poster", font_scale=1.0)
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn scatterplot as base layer for word cloud visualization
sns.scatterplot(
    data=df,
    x="x",
    y="y",
    size="frequency",
    sizes=(300, 3500),
    hue="frequency",
    palette="viridis",
    alpha=0.25,
    legend=False,
    ax=ax,
)

# Add word labels with size based on frequency
max_freq = df["frequency"].max()
min_freq = df["frequency"].min()
freq_range = max_freq - min_freq

colors = sns.color_palette("bright", n_colors=10)
for idx, row in df.iterrows():
    font_size = 18 + (row["frequency"] - min_freq) / freq_range * 30
    color_idx = idx % len(colors)
    ax.text(
        row["x"],
        row["y"],
        row["word"],
        fontsize=font_size,
        fontweight="bold",
        ha="center",
        va="center",
        color=colors[color_idx],
    )

# Clean up axes for word cloud appearance
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.1, 1.2)
ax.axis("off")

# Title following pyplots.ai conventions
fig.suptitle("wordcloud-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", y=0.97)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
