""" pyplots.ai
scatter-connected-temporal: Connected Scatter Plot with Temporal Path
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-13
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Unemployment vs inflation (Phillips curve dynamics, 1990-2023)
np.random.seed(42)
years = np.arange(1990, 2024)
n = len(years)

unemployment = np.array(
    [
        5.6,
        6.8,
        7.5,
        6.9,
        6.1,
        5.6,
        5.4,
        4.9,
        4.5,
        4.2,
        4.0,
        4.7,
        5.8,
        6.0,
        5.5,
        5.1,
        4.6,
        4.6,
        5.8,
        9.3,
        9.6,
        8.9,
        8.1,
        7.4,
        6.2,
        5.3,
        4.9,
        4.4,
        3.9,
        3.7,
        8.1,
        5.4,
        3.6,
        3.6,
    ]
)

inflation = np.array(
    [
        5.4,
        4.2,
        3.0,
        3.0,
        2.6,
        2.8,
        2.9,
        2.3,
        1.6,
        2.2,
        3.4,
        2.8,
        1.6,
        2.3,
        2.7,
        3.4,
        3.2,
        2.8,
        3.8,
        -0.4,
        1.6,
        3.2,
        2.1,
        1.5,
        1.6,
        0.1,
        1.3,
        2.1,
        2.4,
        1.8,
        1.2,
        4.7,
        8.0,
        4.1,
    ]
)

# Build segment-level dataframe for seaborn lineplot with color gradient
seg_records = []
for i in range(n - 1):
    seg_records.append(
        {"Unemployment Rate (%)": unemployment[i], "Inflation Rate (%)": inflation[i], "segment": i, "Year": years[i]}
    )
    seg_records.append(
        {
            "Unemployment Rate (%)": unemployment[i + 1],
            "Inflation Rate (%)": inflation[i + 1],
            "segment": i,
            "Year": years[i],
        }
    )
seg_df = pd.DataFrame(seg_records)

df = pd.DataFrame({"Unemployment Rate (%)": unemployment, "Inflation Rate (%)": inflation, "Year": years})

# Plot setup with seaborn theme
sns.set_theme(style="ticks", rc={"axes.facecolor": "#f7f7f7", "figure.facecolor": "white"})
fig, ax = plt.subplots(figsize=(16, 9))

# Temporal color palette using seaborn's blend palette
palette = sns.color_palette("blend:#a8c4e0,#1a3a5c", n_colors=n)

# Connected path using seaborn lineplot with units for per-segment drawing
sns.lineplot(
    data=seg_df,
    x="Unemployment Rate (%)",
    y="Inflation Rate (%)",
    units="segment",
    hue="Year",
    palette="blend:#a8c4e0,#1a3a5c",
    estimator=None,
    linewidth=2.5,
    legend=False,
    zorder=2,
    ax=ax,
)

# Scatter markers using seaborn scatterplot with temporal hue
sns.scatterplot(
    data=df,
    x="Unemployment Rate (%)",
    y="Inflation Rate (%)",
    hue="Year",
    palette="blend:#a8c4e0,#1a3a5c",
    s=160,
    edgecolor="white",
    linewidth=1.5,
    legend=False,
    zorder=3,
    ax=ax,
)

# Annotate key economic turning points with adjusted positions to avoid crowding
key_points = {
    0: (-20, 18),  # 1990 - start, high inflation
    10: (18, 12),  # 2000 - low unemployment boom
    19: (18, -20),  # 2009 - recession peak unemployment
    22: (-35, -22),  # 2012 - recovery midpoint
    29: (-30, 15),  # 2019 - pre-pandemic low unemployment
    n - 1: (18, -18),  # 2023 - post-pandemic
}

for idx, offset in key_points.items():
    color = palette[idx]
    ax.annotate(
        str(years[idx]),
        (unemployment[idx], inflation[idx]),
        textcoords="offset points",
        xytext=offset,
        fontsize=14,
        fontweight="bold",
        color=color,
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2, "connectionstyle": "arc3,rad=0.15"},
    )

# Axis styling
ax.set_xlabel("Unemployment Rate (%)", fontsize=20)
ax.set_ylabel("Inflation Rate (%)", fontsize=20)
ax.set_title("scatter-connected-temporal \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
sns.despine(ax=ax)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.15, linewidth=0.8)

ax.set_xlim(unemployment.min() - 0.8, unemployment.max() + 0.8)
ax.set_ylim(inflation.min() - 1.0, inflation.max() + 1.0)

# Colorbar for temporal encoding
sm = plt.cm.ScalarMappable(
    cmap=sns.color_palette("blend:#a8c4e0,#1a3a5c", as_cmap=True), norm=plt.Normalize(years[0], years[-1])
)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.02, aspect=30)
cbar.set_label("Year", fontsize=16)
cbar.ax.tick_params(labelsize=14)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
