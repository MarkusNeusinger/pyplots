""" pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-24
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    coord_cartesian,
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
        "Testing",
        "Deployment",
        "Monitoring",
        "Framework",
        "Docker",
        "AWS",
        "Azure",
    ],
    "frequency": [95, 88, 82, 78, 75, 70, 65, 62, 58, 55, 52, 48, 45, 42, 38, 35, 32, 30, 28, 26, 24, 22, 20, 18, 16],
}

df = pd.DataFrame(words_data)

# Calculate font sizes scaled by frequency (range 10-36)
min_freq, max_freq = df["frequency"].min(), df["frequency"].max()
df["size"] = 10 + (df["frequency"] - min_freq) / (max_freq - min_freq) * 26

# Sort by frequency descending
df = df.sort_values("frequency", ascending=False).reset_index(drop=True)

# Hand-crafted positions to ensure no overlap
# Using a carefully planned layout based on word lengths and sizes
# Canvas is 100x56.25 with legend in top-right
positions = [
    (45, 30),  # Python (largest) - center
    (70, 38),  # Data
    (22, 25),  # Machine
    (72, 25),  # Learning
    (30, 38),  # AI
    (55, 18),  # Cloud
    (20, 42),  # API
    (45, 45),  # Database
    (68, 48),  # Security
    (25, 12),  # DevOps
    (50, 8),  # Analytics
    (78, 10),  # Automation
    (8, 30),  # Software
    (88, 32),  # Code
    (35, 52),  # Development
    (60, 52),  # Integration
    (15, 52),  # Platform
    (82, 52),  # Infrastructure
    (8, 18),  # Testing
    (8, 42),  # Deployment
    (55, 38),  # Monitoring
    (85, 42),  # Framework
    (30, 8),  # Docker
    (8, 8),  # AWS
    (75, 8),  # Azure
]

df["x"] = [p[0] for p in positions]
df["y"] = [p[1] for p in positions]

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

# Create legend data - positioned in top right area
legend_df = pd.DataFrame(
    {
        "x": [88, 88, 88, 88],
        "y": [48, 44, 40, 36],
        "label": ["■ High (65+)", "■ Medium (35-64)", "■ Low-Med (15-34)", "■ Low (<15)"],
        "color": ["#306998", "#FFD43B", "#4ECDC4", "#95E1A3"],
    }
)

# Create plot
plot = (
    ggplot(df, aes(x="x", y="y", label="word", size="size", color="color"))
    + geom_text(family="sans-serif", fontstyle="normal", show_legend=False)
    + geom_text(
        data=legend_df, mapping=aes(x="x", y="y", label="label", color="color"), size=9, ha="left", show_legend=False
    )
    + annotate("text", x=88, y=52, label="Frequency", size=11, ha="left", fontweight="bold")
    + scale_size_identity()
    + scale_color_identity()
    + coord_cartesian(xlim=(0, 100), ylim=(0, 56.25))
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
