"""pyplots.ai
pie-portfolio-interactive: Interactive Portfolio Allocation Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="white")
sns.set_context("talk", font_scale=1.2)

# Portfolio data with asset classes and individual holdings
np.random.seed(42)
portfolio_data = pd.DataFrame(
    {
        "asset": [
            "US Large Cap Equity",
            "International Equity",
            "Emerging Markets",
            "US Treasury Bonds",
            "Corporate Bonds",
            "Municipal Bonds",
            "REITs",
            "Gold",
            "Private Equity",
        ],
        "weight": [28.0, 15.0, 7.0, 18.0, 12.0, 5.0, 6.0, 4.0, 5.0],
        "category": [
            "Equities",
            "Equities",
            "Equities",
            "Fixed Income",
            "Fixed Income",
            "Fixed Income",
            "Alternatives",
            "Alternatives",
            "Alternatives",
        ],
        "value": [280000, 150000, 70000, 180000, 120000, 50000, 60000, 40000, 50000],
    }
)

# Category aggregation for outer ring
category_data = portfolio_data.groupby("category").agg({"weight": "sum", "value": "sum"}).reset_index()

# Define color scheme by category
category_colors = {
    "Equities": "#306998",  # Python Blue
    "Fixed Income": "#FFD43B",  # Python Yellow
    "Alternatives": "#4ECDC4",  # Teal
}

# Create shades for individual assets within each category
asset_colors = []
for _, row in portfolio_data.iterrows():
    base_color = category_colors[row["category"]]
    # Get index within category for shade variation
    cat_assets = portfolio_data[portfolio_data["category"] == row["category"]]
    idx = cat_assets[cat_assets["asset"] == row["asset"]].index[0]
    cat_idx = list(cat_assets.index).index(idx)
    # Create slightly varied shades
    color_palette = sns.light_palette(base_color, n_colors=len(cat_assets) + 2, reverse=True)
    asset_colors.append(color_palette[cat_idx + 1])

# Create figure with two concentric rings
fig, ax = plt.subplots(figsize=(14, 12))

# Outer ring - Individual assets (detailed breakdown)
outer_wedges, outer_texts, outer_autotexts = ax.pie(
    portfolio_data["weight"],
    labels=None,
    colors=asset_colors,
    autopct=lambda pct: f"{pct:.1f}%" if pct > 4 else "",
    startangle=90,
    radius=1.0,
    pctdistance=0.82,
    wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 2},
)

# Style outer ring percentages
for autotext in outer_autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight("bold")
    autotext.set_color("#333333")

# Inner ring - Category breakdown
category_colors_list = [category_colors[cat] for cat in category_data["category"]]
inner_wedges, inner_texts, inner_autotexts = ax.pie(
    category_data["weight"],
    labels=None,
    colors=category_colors_list,
    autopct=lambda pct: f"{pct:.0f}%",
    startangle=90,
    radius=0.65,
    pctdistance=0.5,
    wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 2},
)

# Style inner ring percentages
for autotext in inner_autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add center text showing total portfolio value
total_value = portfolio_data["value"].sum()
ax.text(
    0,
    0,
    f"Portfolio\n${total_value / 1000:.0f}K",
    ha="center",
    va="center",
    fontsize=24,
    fontweight="bold",
    color="#333333",
)

# Create detailed annotations (simulating hover tooltips)
# Position annotations around the chart
angles = np.linspace(90, 90 - 360, len(portfolio_data), endpoint=False)
cumulative_weight = 0
annotation_positions = []

for _, row in portfolio_data.iterrows():
    # Calculate angle for this wedge center
    angle_deg = 90 - cumulative_weight - row["weight"] / 2
    cumulative_weight += row["weight"]
    angle_rad = np.deg2rad(angle_deg)

    # Position for annotation (outside the chart)
    x_pos = 1.4 * np.cos(angle_rad)
    y_pos = 1.4 * np.sin(angle_rad)

    annotation_positions.append((x_pos, y_pos, angle_deg))

# Add annotation boxes showing detailed info (simulating interactive tooltips)
# Only show annotations for larger positions to avoid clutter
for i, (_, row) in enumerate(portfolio_data.iterrows()):
    if row["weight"] >= 6:  # Show details for allocations >= 6%
        x_pos, y_pos, angle_deg = annotation_positions[i]

        # Adjust horizontal alignment based on position
        ha = "left" if x_pos > 0 else "right"
        x_offset = 0.1 if x_pos > 0 else -0.1

        annotation_text = f"{row['asset']}\n${row['value']:,.0f} ({row['weight']:.1f}%)"

        # Draw connection line from wedge to annotation
        wedge_x = 1.0 * np.cos(np.deg2rad(angle_deg))
        wedge_y = 1.0 * np.sin(np.deg2rad(angle_deg))

        ax.annotate(
            annotation_text,
            xy=(wedge_x, wedge_y),
            xytext=(x_pos + x_offset, y_pos),
            fontsize=13,
            fontweight="medium",
            ha=ha,
            va="center",
            bbox={
                "boxstyle": "round,pad=0.4",
                "facecolor": "white",
                "edgecolor": category_colors[row["category"]],
                "linewidth": 2,
                "alpha": 0.95,
            },
            arrowprops={"arrowstyle": "-", "color": "#888888", "connectionstyle": "arc3,rad=0.1", "linewidth": 1.5},
        )

# Create legend for categories with detailed info
legend_labels = []
for _, row in category_data.iterrows():
    n_holdings = len(portfolio_data[portfolio_data["category"] == row["category"]])
    legend_labels.append(
        f"{row['category']}: {row['weight']:.0f}% (${row['value'] / 1000:.0f}K, {n_holdings} holdings)"
    )

legend = ax.legend(
    inner_wedges,
    legend_labels,
    title="Asset Classes (Click to Drill Down)",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.12),
    fontsize=14,
    title_fontsize=16,
    frameon=True,
    fancybox=True,
    ncol=3,
    columnspacing=1.5,
)

# Title
ax.set_title("pie-portfolio-interactive · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=30)

# Note about interactivity
ax.text(
    0.5,
    -0.22,
    "Hover over segments to see details • Click asset class to drill down into holdings",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=12,
    fontstyle="italic",
    color="#666666",
)

# Ensure equal aspect ratio
ax.set_aspect("equal")
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.5, 1.5)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
