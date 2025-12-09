"""
ridgeline-basic: Ridgeline Plot
Library: seaborn
"""

import numpy as np
import pandas as pd
import seaborn as sns


# Data - Monthly temperature distributions
np.random.seed(42)
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Generate realistic temperature data with seasonal pattern
data = []
base_temps = [2, 4, 8, 12, 17, 21, 24, 23, 19, 13, 7, 3]  # Typical temperate climate
for i, month in enumerate(months):
    temps = np.random.normal(base_temps[i], 3, 150)
    for t in temps:
        data.append({"month": month, "temperature": t})

df = pd.DataFrame(data)
df["month"] = pd.Categorical(df["month"], categories=months, ordered=True)

# Color palette - gradient from cool to warm
colors = sns.color_palette("coolwarm", n_colors=12)

# Create ridgeline plot using FacetGrid
sns.set_style("white")
g = sns.FacetGrid(
    df,
    row="month",
    hue="month",
    aspect=12,
    height=0.7,
    palette=colors,
    row_order=months[::-1],  # Reverse order so January at bottom
    hue_order=months[::-1],
)

# Draw density plots
g.map(sns.kdeplot, "temperature", bw_adjust=0.8, clip_on=False, fill=True, alpha=0.7, linewidth=1.5)

# Add outline
g.map(sns.kdeplot, "temperature", bw_adjust=0.8, clip_on=False, color="black", lw=1)

# Add horizontal line at y=0
g.refline(y=0, linewidth=1, linestyle="-", color="black", clip_on=False)

# Styling - overlap the rows
g.figure.subplots_adjust(hspace=-0.3)

# Remove axes details
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)

# Add month labels on the left
for i, ax in enumerate(g.axes.flat):
    ax.text(
        -0.02,
        0.1,
        months[::-1][i],
        fontweight="bold",
        fontsize=14,
        color=colors[::-1][i],
        ha="right",
        va="center",
        transform=ax.transAxes,
    )

# Set x-axis label on bottom plot only
g.axes[-1, 0].set_xlabel("Temperature (°C)", fontsize=16)
g.axes[-1, 0].tick_params(axis="x", labelsize=12)

# Title
g.figure.suptitle("Monthly Temperature Distribution", fontsize=20, fontweight="bold", y=0.98)

# Save
g.figure.set_size_inches(16, 9)
g.savefig("plot.png", dpi=300, bbox_inches="tight")
