""" pyplots.ai
cartogram-area-distortion: Cartogram with Area Distortion by Data Value
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 78/100 | Created: 2026-03-13
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: US states with population (millions) and grid positions
# Tile cartogram where each tile's size is proportional to population
np.random.seed(42)

states_data = {
    # (row, col, population_millions, region)
    # Row 0
    "WA": (0, 1, 7.7, "West"),
    "MT": (0, 3, 1.1, "West"),
    "ND": (0, 5, 0.8, "Midwest"),
    "MN": (0, 6, 5.7, "Midwest"),
    "WI": (0, 7, 5.9, "Midwest"),
    "MI": (0, 8, 10.0, "Midwest"),
    "NY": (0, 10, 19.5, "Northeast"),
    "VT": (0, 11, 0.6, "Northeast"),
    "ME": (0, 12, 1.4, "Northeast"),
    # Row 1
    "OR": (1, 1, 4.2, "West"),
    "ID": (1, 2, 1.9, "West"),
    "WY": (1, 3, 0.6, "West"),
    "SD": (1, 5, 0.9, "Midwest"),
    "IA": (1, 6, 3.2, "Midwest"),
    "IL": (1, 7, 12.6, "Midwest"),
    "IN": (1, 8, 6.8, "Midwest"),
    "OH": (1, 9, 11.8, "Midwest"),
    "PA": (1, 10, 13.0, "Northeast"),
    "MA": (1, 11, 7.0, "Northeast"),
    "NH": (1, 12, 1.4, "Northeast"),
    # Row 2
    "NV": (2, 1, 3.1, "West"),
    "UT": (2, 2, 3.3, "West"),
    "CO": (2, 3, 5.8, "West"),
    "NE": (2, 5, 2.0, "Midwest"),
    "KS": (2, 6, 2.9, "Midwest"),
    "MO": (2, 7, 6.2, "Midwest"),
    "KY": (2, 8, 4.5, "South"),
    "WV": (2, 9, 1.8, "South"),
    "VA": (2, 10, 8.6, "South"),
    "MD": (2, 11, 6.2, "South"),
    "NJ": (2, 12, 9.3, "Northeast"),
    # Row 3
    "CA": (3, 1, 39.0, "West"),
    "AZ": (3, 2, 7.3, "West"),
    "NM": (3, 3, 2.1, "West"),
    "OK": (3, 5, 4.0, "South"),
    "AR": (3, 6, 3.0, "South"),
    "TN": (3, 7, 7.0, "South"),
    "NC": (3, 9, 10.6, "South"),
    "SC": (3, 10, 5.2, "South"),
    "DE": (3, 11, 1.0, "Northeast"),
    "CT": (3, 12, 3.6, "Northeast"),
    # Row 4
    "TX": (4, 3, 29.5, "South"),
    "LA": (4, 5, 4.6, "South"),
    "MS": (4, 6, 3.0, "South"),
    "AL": (4, 7, 5.0, "South"),
    "GA": (4, 8, 10.8, "South"),
    "FL": (4, 10, 22.2, "South"),
    "RI": (4, 12, 1.1, "Northeast"),
    # Row 5
    "AK": (5, 0, 0.7, "West"),
    "HI": (5, 2, 1.4, "West"),
}

# Build dataframe
rows = []
for state, (r, c, pop, region) in states_data.items():
    rows.append({"state": state, "row": r, "col": c, "population": pop, "region": region})
df = pd.DataFrame(rows)

# Scale tile sizes: area proportional to population
# Map population to tile side length (sqrt for area proportionality)
max_pop = df["population"].max()
min_scale = 0.25
max_scale = 0.95
df["tile_size"] = min_scale + (max_scale - min_scale) * np.sqrt(df["population"] / max_pop)

# Region color palette
region_colors = {"West": "#306998", "Midwest": "#5AAE61", "South": "#E07B53", "Northeast": "#9D6AB8"}

# Plot
sns.set_theme(style="white", context="talk", font_scale=1.1)
fig, ax = plt.subplots(figsize=(16, 9))

# Draw each state as a variably-sized tile centered on its grid position
for _, row in df.iterrows():
    cx = row["col"]
    cy = row["row"]
    size = row["tile_size"]
    color = region_colors[row["region"]]

    # Draw tile centered on grid position
    rect = mpatches.FancyBboxPatch(
        (cx - size / 2, cy - size / 2),
        size,
        size,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor="white",
        linewidth=2,
        alpha=0.85,
        zorder=2,
    )
    ax.add_patch(rect)

    # State abbreviation
    fontsize = max(10, min(20, int(12 + size * 8)))
    ax.text(
        cx,
        cy - 0.05,
        row["state"],
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color="white",
        zorder=3,
    )

    # Population value (show for larger tiles)
    if row["population"] >= 3.0:
        ax.text(
            cx,
            cy + 0.22,
            f"{row['population']:.0f}M",
            ha="center",
            va="center",
            fontsize=max(8, int(fontsize * 0.65)),
            color="white",
            alpha=0.9,
            zorder=3,
        )

# Axis limits with padding
ax.set_xlim(-1.2, 13.5)
ax.set_ylim(-0.8, 6.2)
ax.invert_yaxis()
ax.set_aspect("equal")

# Remove all axes
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Background
fig.patch.set_facecolor("#f5f5f5")
ax.set_facecolor("#f5f5f5")

# Title
ax.set_title(
    "US States by Population · cartogram-area-distortion · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)

# Region legend
legend_patches = [
    mpatches.Patch(facecolor=color, edgecolor="white", label=region, alpha=0.85)
    for region, color in region_colors.items()
]
ax.legend(
    handles=legend_patches,
    loc="lower left",
    fontsize=15,
    title="Region",
    title_fontsize=17,
    framealpha=0.95,
    edgecolor="#cccccc",
)

# Size reference annotation
ax.text(
    0.98,
    0.02,
    "Tile area ∝ state population",
    ha="right",
    va="bottom",
    fontsize=14,
    color="#666666",
    fontstyle="italic",
    transform=ax.transAxes,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
