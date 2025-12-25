"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data - Market share by company (highlighting the leader)
categories = ["TechCorp", "DataSoft", "CloudNet", "AIVentures", "CyberSys"]
values = [35.2, 22.8, 18.5, 14.3, 9.2]
explode = [0.1, 0, 0, 0, 0]  # Explode the market leader

# Create color palette using seaborn
colors = sns.color_palette(["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3"])

# Create figure (square format for pie chart)
fig, ax = plt.subplots(figsize=(12, 12))

# Create exploded pie chart
wedges, texts, autotexts = ax.pie(
    values,
    explode=explode,
    labels=None,
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.65,
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    textprops={"fontsize": 20, "fontweight": "bold"},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(18)
    autotext.set_fontweight("bold")

# Add legend with seaborn styling
legend = ax.legend(
    wedges,
    [f"{cat} ({val}%)" for cat, val in zip(categories, values, strict=True)],
    title="Company",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=16,
    title_fontsize=18,
    frameon=True,
    fancybox=True,
    shadow=True,
)

# Title
ax.set_title("Market Share Analysis · pie-exploded · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Ensure equal aspect ratio for circular pie
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
