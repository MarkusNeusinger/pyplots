"""
wordcloud-basic: Basic Word Cloud
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_rect,
    element_text,
    geom_text,
    ggplot,
    labs,
    scale_color_identity,
    scale_size_identity,
    theme,
)


# Word frequency data - technology survey responses
np.random.seed(42)
words_data = {
    "word": [
        "Python",
        "Data",
        "Machine",
        "Learning",
        "AI",
        "Cloud",
        "API",
        "Database",
        "Security",
        "DevOps",
        "Analytics",
        "Automation",
        "Software",
        "Code",
        "Development",
        "Integration",
        "Platform",
        "Infrastructure",
        "Performance",
        "Scalability",
        "Testing",
        "Deployment",
        "Monitoring",
        "Architecture",
        "Framework",
        "Microservices",
        "Container",
        "Kubernetes",
        "Docker",
        "AWS",
        "Azure",
        "Innovation",
        "Digital",
        "Transform",
        "Agile",
    ],
    "frequency": [
        95,
        88,
        82,
        78,
        75,
        70,
        65,
        62,
        58,
        55,
        52,
        48,
        45,
        42,
        38,
        35,
        32,
        30,
        28,
        26,
        24,
        22,
        20,
        18,
        16,
        14,
        13,
        12,
        11,
        10,
        9,
        8,
        7,
        6,
        5,
    ],
}

df = pd.DataFrame(words_data)

# Calculate font sizes scaled by frequency (range 10-36 for readability)
min_freq, max_freq = df["frequency"].min(), df["frequency"].max()
df["size"] = 10 + (df["frequency"] - min_freq) / (max_freq - min_freq) * 26

# Sort by frequency descending for placement (largest words first)
df = df.sort_values("frequency", ascending=False).reset_index(drop=True)

# Fixed positions using concentric rings to guarantee no overlaps
np.random.seed(42)
width, height = 100, 56.25
center_x, center_y = width / 2, height / 2

# Define rings with word counts: inner ring has fewer, larger words
rings = [
    {"count": 5, "radius": 0, "y_offset": 0},  # Center - 5 largest words
    {"count": 8, "radius": 16, "y_offset": 0},  # Ring 1
    {"count": 10, "radius": 28, "y_offset": 0},  # Ring 2
    {"count": 12, "radius": 40, "y_offset": 0},  # Ring 3 (outer)
]

positions_x = []
positions_y = []
word_idx = 0

# Place center words in a horizontal line with spacing
center_words = 5
center_spacing = 14
center_start_x = center_x - (center_words - 1) * center_spacing / 2
for i in range(center_words):
    x = center_start_x + i * center_spacing
    y = center_y
    positions_x.append(x)
    positions_y.append(y)
word_idx = center_words

# Place remaining words in concentric rings
for ring in rings[1:]:
    ring_count = min(ring["count"], len(df) - word_idx)
    if ring_count <= 0:
        break
    for i in range(ring_count):
        angle = (2 * np.pi * i / ring_count) + np.random.uniform(-0.1, 0.1)
        # Adjust radius based on 16:9 aspect ratio
        x = center_x + ring["radius"] * np.cos(angle) * 1.1
        y = center_y + ring["radius"] * np.sin(angle) * 0.6

        # Keep within bounds
        x = np.clip(x, 12, width - 12)
        y = np.clip(y, 6, height - 6)

        positions_x.append(x)
        positions_y.append(y)
    word_idx += ring_count

df = df.head(len(positions_x))
df["x"] = positions_x
df["y"] = positions_y

# Assign colors based on frequency tiers
colors = []
for freq in df["frequency"]:
    if freq >= 65:
        colors.append("#306998")  # Python Blue - high frequency
    elif freq >= 35:
        colors.append("#FFD43B")  # Python Yellow - medium frequency
    elif freq >= 15:
        colors.append("#4ECDC4")  # Teal - lower medium
    else:
        colors.append("#95E1A3")  # Light green - low frequency
df["color"] = colors

# Create plot
plot = (
    ggplot(df, aes(x="x", y="y", label="word", size="size", color="color"))
    + geom_text(family="sans-serif", fontstyle="normal", show_legend=False)
    + scale_size_identity()
    + scale_color_identity()
    + labs(title="Tech Survey Keywords · wordcloud-basic · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center", weight="bold", margin={"b": 15}),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        axis_text=element_blank(),
        axis_title=element_blank(),
        axis_ticks=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
