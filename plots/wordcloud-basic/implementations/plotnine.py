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
        "Sprint",
        "Scrum",
        "Pipeline",
        "Algorithm",
        "Neural",
        "Network",
        "Deep",
        "Model",
        "Training",
        "Dataset",
        "Feature",
        "Prediction",
        "Insight",
        "Dashboard",
        "Report",
    ],
    "frequency": [
        95,
        88,
        82,
        80,
        78,
        72,
        70,
        68,
        65,
        62,
        60,
        58,
        55,
        53,
        50,
        48,
        46,
        44,
        42,
        40,
        38,
        36,
        34,
        32,
        30,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
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
        4,
    ],
}

df = pd.DataFrame(words_data)

# Calculate font sizes scaled by frequency (range 8-45 for visibility at 4800x2700)
min_freq, max_freq = df["frequency"].min(), df["frequency"].max()
df["size"] = 8 + (df["frequency"] - min_freq) / (max_freq - min_freq) * 37


# Word placement using Archimedean spiral for classic word cloud look
def place_words(words_df, width=100, height=56.25):
    """Place words in expanding spiral from center."""
    positions = []
    np.random.seed(42)

    # Sort by frequency descending
    sorted_df = words_df.sort_values("frequency", ascending=False).reset_index(drop=True)

    center_x, center_y = width / 2, height / 2

    for i, row in sorted_df.iterrows():
        # Archimedean spiral: r = a + b*theta
        theta = i * 0.7  # Angle increment
        r = 2 + i * 0.85  # Radius grows with index (reduced for tighter fit)

        # Adjust for 16:9 aspect ratio
        x = center_x + r * np.cos(theta) * 1.8
        y = center_y + r * np.sin(theta) * 1.1

        # Add slight randomness for natural look
        x += np.random.uniform(-1.0, 1.0)
        y += np.random.uniform(-0.5, 0.5)

        # Keep within bounds - estimate word width based on character count and size
        word_len = len(row["word"])
        est_width = word_len * row["size"] * 0.12  # Approximate width
        margin_x = max(12, est_width / 2 + 2)
        margin_y = max(5, row["size"] * 0.2)
        x = np.clip(x, margin_x, width - margin_x)
        y = np.clip(y, margin_y, height - margin_y)

        positions.append({"word": row["word"], "x": x, "y": y, "size": row["size"], "frequency": row["frequency"]})

    return pd.DataFrame(positions)


# Calculate positions
plot_df = place_words(df)


# Assign colors based on frequency tiers
def assign_color(freq):
    if freq >= 70:
        return "#306998"  # Python Blue - high frequency
    elif freq >= 40:
        return "#FFD43B"  # Python Yellow - medium frequency
    elif freq >= 20:
        return "#4ECDC4"  # Teal - lower medium
    else:
        return "#95E1A3"  # Light green - low frequency


plot_df["color"] = plot_df["frequency"].apply(assign_color)

# Create plot
plot = (
    ggplot(plot_df, aes(x="x", y="y", label="word", size="size", color="color"))
    + geom_text(fontweight="bold", show_legend=False)
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
