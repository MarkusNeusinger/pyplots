"""pyplots.ai
choropleth-basic: Choropleth Map with Regional Coloring
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: US states grid representation with economic data (GDP growth rate %)
# Using a stylized grid layout that approximates US geography
np.random.seed(42)

# State data with grid positions (row, col) approximating US map layout
# Values represent GDP growth rate (%)
states_data = {
    # Row 0 (top - Pacific Northwest, Northern states)
    "WA": (0, 0, 3.2),
    "MT": (0, 2, 1.8),
    "ND": (0, 4, 2.1),
    "MN": (0, 5, 2.9),
    "WI": (0, 6, 2.3),
    "MI": (0, 7, 1.9),
    "NY": (0, 9, 3.5),
    "VT": (0, 10, 1.5),
    "ME": (0, 11, 1.2),
    # Row 1
    "OR": (1, 0, 2.8),
    "ID": (1, 1, 3.1),
    "WY": (1, 2, 0.9),
    "SD": (1, 4, 1.7),
    "IA": (1, 5, 2.0),
    "IL": (1, 6, 2.5),
    "IN": (1, 7, 2.2),
    "OH": (1, 8, 1.8),
    "PA": (1, 9, 2.1),
    "MA": (1, 10, 3.8),
    "NH": (1, 11, 2.4),
    # Row 2
    "NV": (2, 0, 4.1),
    "UT": (2, 1, 4.5),
    "CO": (2, 2, 3.9),
    "NE": (2, 4, 1.6),
    "KS": (2, 5, 1.4),
    "MO": (2, 6, 1.9),
    "KY": (2, 7, 2.0),
    "WV": (2, 8, 0.5),
    "VA": (2, 9, 3.2),
    "MD": (2, 10, 2.8),
    "NJ": (2, 11, 2.6),
    # Row 3
    "CA": (3, 0, 3.7),
    "AZ": (3, 1, 4.2),
    "NM": (3, 2, 1.3),
    "OK": (3, 4, 1.1),
    "AR": (3, 5, 1.5),
    "TN": (3, 6, 3.0),
    "NC": (3, 8, 3.4),
    "SC": (3, 9, 2.7),
    "DE": (3, 10, 2.3),
    "CT": (3, 11, 2.9),
    # Row 4 (bottom - Southern states)
    "TX": (4, 2, 3.6),
    "LA": (4, 4, 0.8),
    "MS": (4, 5, 0.6),
    "AL": (4, 6, 1.7),
    "GA": (4, 7, 3.3),
    "FL": (4, 9, 3.8),
    "RI": (4, 11, 2.0),
    # Alaska and Hawaii (offset)
    "AK": (5, 0, 0.4),
    "HI": (5, 1, 2.5),
}

# Create DataFrame
df = pd.DataFrame(
    [(k, v[0], v[1], v[2]) for k, v in states_data.items()], columns=["state", "row", "col", "gdp_growth"]
)

# Create grid matrix for heatmap (6 rows x 12 cols)
grid = np.full((6, 12), np.nan)
state_labels = np.full((6, 12), "", dtype=object)

for _, row in df.iterrows():
    grid[int(row["row"]), int(row["col"])] = row["gdp_growth"]
    state_labels[int(row["row"]), int(row["col"])] = row["state"]

# Set up seaborn styling
sns.set_theme(style="white", context="talk", font_scale=1.1)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create heatmap using seaborn with masked values for empty cells
mask = np.isnan(grid)
heatmap = sns.heatmap(
    grid,
    mask=mask,
    cmap="YlGnBu",
    annot=state_labels,
    fmt="",
    annot_kws={"size": 18, "weight": "bold", "color": "#1a1a1a"},
    cbar=True,
    cbar_kws={"label": "GDP Growth Rate (%)", "shrink": 0.8, "aspect": 25, "pad": 0.02},
    linewidths=3,
    linecolor="white",
    square=True,
    vmin=0,
    vmax=5,
    ax=ax,
)

# Customize colorbar
cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.set_label("GDP Growth Rate (%)", fontsize=18)

# Add value annotations below state labels for cells with data
for i in range(6):
    for j in range(12):
        if not np.isnan(grid[i, j]):
            ax.text(
                j + 0.5,
                i + 0.73,
                f"{grid[i, j]:.1f}%",
                ha="center",
                va="center",
                fontsize=13,
                color="#333333",
                fontweight="medium",
            )

# Styling
ax.set_title("US States Economic Growth · choropleth-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

# Remove axis labels and ticks (geographic grid doesn't need them)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")

# Add subtitle explaining the visualization
ax.text(
    0.5,
    -0.05,
    "Stylized grid representation of US states colored by annual GDP growth rate",
    ha="center",
    va="top",
    fontsize=14,
    color="#666666",
    transform=ax.transAxes,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
