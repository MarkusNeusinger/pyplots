"""
pie-basic: Basic Pie Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

wedges, texts, autotexts = ax.pie(
    data["value"],
    labels=data["category"],
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.02] * len(data),
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
)

# Style the text
for text in texts:
    text.set_fontsize(20)
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color("white")
    autotext.set_fontweight("bold")

ax.set_title("Basic Pie Chart", fontsize=20, fontweight="bold", pad=20)

# Equal aspect ratio ensures circular pie
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
