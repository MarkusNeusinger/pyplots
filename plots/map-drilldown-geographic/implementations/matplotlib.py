"""pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection


# Data: Three-level hierarchy showing drill-down from World → USA → California
# Level 1: World regions with sales data (in billions USD)
world_regions = {"North America": 245, "South America": 68, "Europe": 189, "Africa": 42, "Asia": 312, "Oceania": 34}

# Level 2: US states with sales data (in millions USD) - drill into North America
us_states = {
    "California": 42500,
    "Texas": 31200,
    "New York": 28900,
    "Florida": 19800,
    "Illinois": 16500,
    "Pennsylvania": 14200,
    "Ohio": 12800,
    "Georgia": 11500,
    "Michigan": 10200,
    "Washington": 9800,
}

# Level 3: California cities with sales data (in millions USD) - drill into California
ca_cities = {
    "Los Angeles": 12800,
    "San Francisco": 8600,
    "San Diego": 5200,
    "San Jose": 4800,
    "Sacramento": 2400,
    "Oakland": 2100,
    "Fresno": 1800,
    "Long Beach": 1600,
    "Irvine": 1400,
    "Santa Monica": 1200,
}

# Create figure with 3 panels (1 row, 3 columns) for the hierarchy
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor("white")

# Create gridspec for better layout control
gs = fig.add_gridspec(1, 3, left=0.04, right=0.88, top=0.85, bottom=0.12, wspace=0.15)
axes = [fig.add_subplot(gs[0, i]) for i in range(3)]

# Color setup
cmap = plt.cm.Blues


# Helper function to create tile grid choropleth
def create_tile_choropleth(ax, data, positions, labels, level_label, breadcrumb, highlight=None):
    """Create a tile-based choropleth for one hierarchy level."""
    values = list(data.values())
    vmin, vmax = min(values), max(values)

    patches = []
    colors = []
    names_list = list(positions.keys())

    for name in names_list:
        col, row = positions[name]
        rect = mpatches.FancyBboxPatch(
            (col * 1.2, row * 1.2),
            1.0,
            1.0,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            linewidth=2,
            edgecolor="white",
        )
        patches.append(rect)
        value = data.get(name, 0)
        norm_value = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
        colors.append(cmap(0.2 + norm_value * 0.7))  # Range 0.2-0.9 for better contrast

    collection = PatchCollection(patches, facecolors=colors, edgecolors="white", linewidths=2)
    ax.add_collection(collection)

    # Add labels
    for name in names_list:
        col, row = positions[name]
        value = data.get(name, 0)
        norm_value = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
        text_color = "white" if norm_value > 0.4 else "#306998"

        # Abbreviate long names
        display_name = labels.get(name, name[:3].upper())
        ax.text(
            col * 1.2 + 0.5,
            row * 1.2 + 0.5,
            display_name,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=text_color,
        )

    # Highlight the region that drills down (with a border)
    if highlight and highlight in positions:
        hcol, hrow = positions[highlight]
        highlight_rect = mpatches.FancyBboxPatch(
            (hcol * 1.2 - 0.05, hrow * 1.2 - 0.05),
            1.1,
            1.1,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=4,
            edgecolor="#FFD43B",
            facecolor="none",
            zorder=10,
        )
        ax.add_patch(highlight_rect)

    # Styling
    ax.set_aspect("equal")
    ax.axis("off")

    # Level indicator at the top
    ax.set_title(level_label, fontsize=15, fontweight="bold", color="#306998", pad=10)

    # Breadcrumb navigation at the bottom
    ax.text(0.5, -0.08, breadcrumb, transform=ax.transAxes, ha="center", fontsize=11, color="#555555", style="italic")

    return vmin, vmax


# Panel 1: World regions
world_positions = {
    "North America": (1, 2),
    "South America": (1, 0),
    "Europe": (2, 2),
    "Africa": (2, 1),
    "Asia": (3, 2),
    "Oceania": (3, 0),
}
world_labels = {
    "North America": "N.AM",
    "South America": "S.AM",
    "Europe": "EUR",
    "Africa": "AFR",
    "Asia": "ASIA",
    "Oceania": "OCE",
}

axes[0].set_xlim(0.5, 5.5)
axes[0].set_ylim(-0.5, 4.0)
create_tile_choropleth(
    axes[0], world_regions, world_positions, world_labels, "Level 1: Regions", "World", highlight="North America"
)

# Panel 2: US states (drill into North America)
state_positions = {
    "California": (0, 2),
    "Washington": (0, 3),
    "Texas": (1, 1),
    "Florida": (2, 0),
    "Illinois": (1, 2),
    "New York": (2, 3),
    "Pennsylvania": (2, 2),
    "Ohio": (1, 3),
    "Georgia": (2, 1),
    "Michigan": (0, 4),
}
state_labels = {
    "California": "CA",
    "Washington": "WA",
    "Texas": "TX",
    "Florida": "FL",
    "Illinois": "IL",
    "New York": "NY",
    "Pennsylvania": "PA",
    "Ohio": "OH",
    "Georgia": "GA",
    "Michigan": "MI",
}

axes[1].set_xlim(-0.5, 4.0)
axes[1].set_ylim(-0.8, 6.2)
create_tile_choropleth(
    axes[1],
    us_states,
    state_positions,
    state_labels,
    "Level 2: States",
    "World > United States",
    highlight="California",
)

# Panel 3: California cities (drill into California)
city_positions = {
    "Los Angeles": (1, 1),
    "San Francisco": (0, 3),
    "San Diego": (1, 0),
    "San Jose": (0, 2),
    "Sacramento": (1, 3),
    "Oakland": (0, 4),
    "Fresno": (1, 2),
    "Long Beach": (2, 1),
    "Irvine": (2, 0),
    "Santa Monica": (0, 1),
}
city_labels = {
    "Los Angeles": "LA",
    "San Francisco": "SF",
    "San Diego": "SD",
    "San Jose": "SJ",
    "Sacramento": "SAC",
    "Oakland": "OAK",
    "Fresno": "FRE",
    "Long Beach": "LB",
    "Irvine": "IRV",
    "Santa Monica": "SM",
}

axes[2].set_xlim(-0.5, 4.0)
axes[2].set_ylim(-0.8, 6.2)
create_tile_choropleth(
    axes[2],
    ca_cities,
    city_positions,
    city_labels,
    "Level 3: Cities",
    "World > United States > California",
    highlight=None,  # No further drill-down from cities
)

# Add colorbar for the entire figure
cbar_ax = fig.add_axes([0.91, 0.20, 0.018, 0.50])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)
cbar.set_label("Sales Value (relative)", fontsize=14)
cbar.ax.tick_params(labelsize=11)
cbar.set_ticks([0, 0.5, 1])
cbar.set_ticklabels(["Low", "Medium", "High"])

# Add drill-down arrows between panels
arrow_style = {"arrowstyle": "-|>", "color": "#FFD43B", "lw": 4, "mutation_scale": 25}
for i in range(2):
    # Get position between panels
    x_start = axes[i].get_position().x1 + 0.01
    x_end = axes[i + 1].get_position().x0 - 0.01
    x_mid = (x_start + x_end) / 2
    y_mid = 0.48

    # Draw arrow
    fig.patches.append(
        mpatches.FancyArrowPatch((x_start, y_mid), (x_end, y_mid), transform=fig.transFigure, **arrow_style, zorder=100)
    )

# Main title
fig.suptitle("map-drilldown-geographic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.96)

# Subtitle explaining the drill-down concept
fig.text(
    0.46,
    0.90,
    "Hierarchical drill-down: Click regions to explore finer geographic detail",
    ha="center",
    fontsize=14,
    color="#666666",
    style="italic",
)

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
