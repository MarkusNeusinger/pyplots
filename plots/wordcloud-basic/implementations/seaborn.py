"""pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set random seed for reproducibility
np.random.seed(42)

# Data - Tech industry survey responses about skills (30 words)
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
    "CICD": 35,
    "Azure": 30,
    "MongoDB": 28,
    "Redis": 26,
    "GraphQL": 24,
    "Terraform": 22,
    "Spark": 20,
    "Analytics": 18,
    "Backend": 16,
}

# Sort by frequency descending for placement priority
sorted_pairs = sorted(word_frequencies.items(), key=lambda x: -x[1])
words = [p[0] for p in sorted_pairs]
frequencies = [p[1] for p in sorted_pairs]
n_words = len(words)

# Calculate font sizes with better differentiation (14pt to 58pt range)
freq_array = np.array(frequencies)
max_freq, min_freq = freq_array.max(), freq_array.min()
freq_range = max_freq - min_freq
font_sizes = 14 + (freq_array - min_freq) / freq_range * 44

# Spiral placement algorithm to avoid overlaps
placed_boxes = []


def get_text_bbox(x, y, word, fsize):
    """Estimate bounding box for text (width based on char count, height on font size)."""
    char_width = fsize * 0.012
    width = len(word) * char_width
    height = fsize * 0.022
    return (x - width / 2, y - height / 2, x + width / 2, y + height / 2)


def boxes_overlap(box1, box2, padding=0.03):
    """Check if two boxes overlap with padding."""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    return not (
        x1_max + padding < x2_min or x2_max + padding < x1_min or y1_max + padding < y2_min or y2_max + padding < y1_min
    )


def find_position(word, fsize, placed):
    """Find non-overlapping position using spiral search."""
    # Start from center and spiral outward
    for radius in np.linspace(0, 1.6, 80):
        for angle in np.linspace(0, 2 * np.pi, max(8, int(radius * 20))):
            x = radius * np.cos(angle) * 1.1
            y = radius * np.sin(angle) * 0.55
            bbox = get_text_bbox(x, y, word, fsize)
            # Check bounds
            if bbox[0] < -1.7 or bbox[2] > 1.7 or bbox[1] < -0.85 or bbox[3] > 0.85:
                continue
            # Check overlaps
            overlap = False
            for pb in placed:
                if boxes_overlap(bbox, pb):
                    overlap = True
                    break
            if not overlap:
                return x, y, bbox
    # Fallback - place at edge
    return 1.5, 0.7 - len(placed) * 0.1, get_text_bbox(1.5, 0.7 - len(placed) * 0.1, word, fsize)


# Place words using spiral algorithm
x_positions = []
y_positions = []
for word, fsize in zip(words, font_sizes, strict=True):
    x, y, bbox = find_position(word, fsize, placed_boxes)
    x_positions.append(x)
    y_positions.append(y)
    placed_boxes.append(bbox)

# Create DataFrame
df = pd.DataFrame({"word": words, "frequency": frequencies, "x": x_positions, "y": y_positions, "fontsize": font_sizes})

# Plot using seaborn
sns.set_theme(style="white", context="poster", font_scale=1.0)
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn scatterplot as subtle background layer
sns.scatterplot(
    data=df,
    x="x",
    y="y",
    size="frequency",
    sizes=(200, 2500),
    hue="frequency",
    palette="viridis",
    alpha=0.15,
    legend=False,
    ax=ax,
)

# Add word labels with frequency-based sizing and seaborn palette colors
colors = sns.color_palette("husl", n_colors=n_words)
for idx, row_data in df.iterrows():
    ax.text(
        row_data["x"],
        row_data["y"],
        row_data["word"],
        fontsize=row_data["fontsize"],
        fontweight="bold",
        ha="center",
        va="center",
        color=colors[idx],
    )

# Clean up axes for word cloud appearance
ax.set_xlim(-1.9, 1.9)
ax.set_ylim(-1.0, 1.05)
ax.axis("off")

# Title following exact pyplots.ai format
ax.set_title("wordcloud-basic · seaborn · pyplots.ai", fontsize=26, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
