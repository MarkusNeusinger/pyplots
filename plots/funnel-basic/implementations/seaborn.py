""" pyplots.ai
funnel-basic: Basic Funnel Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - Sales funnel example
stages = ["Awareness", "Interest", "Consideration", "Intent", "Purchase"]
values = [1000, 600, 400, 200, 100]
max_value = max(values)

# Create dataframe
df = pd.DataFrame({"stage": stages, "value": values, "percentage": [v / values[0] * 100 for v in values]})

# Seaborn styling
sns.set_theme(style="white")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Color palette using Python Blue and Yellow
colors = ["#306998", "#4078A8", "#6AA8D1", "#FFD43B", "#E8C547"]

# Create horizontal bar chart using seaborn barplot
sns.barplot(
    data=df,
    y="stage",
    x="value",
    hue="stage",
    palette=colors,
    ax=ax,
    dodge=False,
    legend=False,
    order=stages,
    hue_order=stages,
    edgecolor="white",
    linewidth=3,
    width=0.85,
)

# Center the bars by adjusting xlim and moving bars
# Get current bar positions and shift them to center
for bar in ax.patches:
    bar_width = bar.get_width()
    # Shift bar to center it (move left edge to -width/2)
    bar.set_x(-bar_width / 2)

# Remove axis decorations
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(left=False, bottom=False, labelbottom=False)
for spine in ax.spines.values():
    spine.set_visible(False)

# Style y-axis labels (stage names) - move them to the left
ax.tick_params(axis="y", labelsize=20, pad=15)

# Add value and percentage labels on each bar
for i, (value, pct) in enumerate(zip(values, df["percentage"], strict=True)):
    label_text = f"{value:,} ({pct:.0f}%)"
    # Choose text color based on background brightness
    text_color = "white" if i < 3 else "#333333"
    ax.text(0, i, label_text, ha="center", va="center", fontsize=18, fontweight="bold", color=text_color)

# Set symmetric x limits for centered funnel look
ax.set_xlim(-max_value / 2 * 1.15, max_value / 2 * 1.15)

# Title
ax.set_title("funnel-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
