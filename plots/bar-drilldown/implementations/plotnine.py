"""pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-16
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_bar,
    geom_segment,
    geom_text,
    ggplot,
    guides,
    labs,
    scale_fill_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


np.random.seed(42)

# Hierarchical data: Sales by region and country
hierarchy_data = [
    # Root level (Regions)
    {"id": "americas", "name": "Americas", "parent": None, "value": 0},
    {"id": "europe", "name": "Europe", "parent": None, "value": 0},
    {"id": "asia", "name": "Asia Pacific", "parent": None, "value": 0},
    {"id": "mea", "name": "MEA", "parent": None, "value": 0},
    # Level 2: Americas countries
    {"id": "usa", "name": "USA", "parent": "americas", "value": 450},
    {"id": "canada", "name": "Canada", "parent": "americas", "value": 120},
    {"id": "brazil", "name": "Brazil", "parent": "americas", "value": 85},
    {"id": "mexico", "name": "Mexico", "parent": "americas", "value": 65},
    # Level 2: Europe countries
    {"id": "uk", "name": "UK", "parent": "europe", "value": 180},
    {"id": "germany", "name": "Germany", "parent": "europe", "value": 210},
    {"id": "france", "name": "France", "parent": "europe", "value": 145},
    {"id": "spain", "name": "Spain", "parent": "europe", "value": 75},
    # Level 2: Asia Pacific countries
    {"id": "china", "name": "China", "parent": "asia", "value": 320},
    {"id": "japan", "name": "Japan", "parent": "asia", "value": 195},
    {"id": "australia", "name": "Australia", "parent": "asia", "value": 88},
    {"id": "india", "name": "India", "parent": "asia", "value": 110},
    # Level 2: MEA countries
    {"id": "uae", "name": "UAE", "parent": "mea", "value": 95},
    {"id": "south_africa", "name": "S. Africa", "parent": "mea", "value": 55},
    {"id": "saudi", "name": "Saudi Arabia", "parent": "mea", "value": 70},
]

df = pd.DataFrame(hierarchy_data)

# Calculate parent values (sum of children)
regions = ["americas", "europe", "asia", "mea"]
for region in regions:
    region_total = df[df["parent"] == region]["value"].sum()
    df.loc[df["id"] == region, "value"] = region_total

# Prepare data for top-level view (regions only)
top_level_df = df[df["parent"].isna()].copy()
top_level_df = top_level_df.sort_values("value", ascending=False)
top_level_df["x"] = range(len(top_level_df))
top_level_df["panel"] = "Region"

# Prepare data for drilled-down view (Americas breakdown)
drilled_df = df[df["parent"] == "americas"].copy()
drilled_df = drilled_df.sort_values("value", ascending=False)
drilled_df["x"] = [x + 5.5 for x in range(len(drilled_df))]  # Offset to create gap
drilled_df["panel"] = "Americas"

# Combine for single panel display
combined_df = pd.concat([top_level_df, drilled_df], ignore_index=True)

# Define colors for each category
region_colors = {
    "Americas": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Asia Pacific": "#4B8BBE",  # Light Blue
    "MEA": "#E07B39",  # Orange
    # Drilled countries (Americas shades)
    "USA": "#1A4A6E",  # Darker blue
    "Canada": "#306998",
    "Brazil": "#4B8BBE",
    "Mexico": "#7FB3D5",
}

# Create annotation data for drill arrow
arrow_df = pd.DataFrame({"x_start": [0], "x_end": [5.5], "y_start": [750], "y_end": [480]})

# Section labels data
section_labels = pd.DataFrame({"x": [1.5, 7], "y": [850, 850], "label": ["All Regions", "All > Americas"]})

# Create the plot using single panel with custom x positioning
plot = (
    ggplot(combined_df, aes(x="x", y="value"))
    + geom_bar(aes(fill="name"), stat="identity", width=0.8)
    + geom_text(aes(label="value", y="value"), va="bottom", size=12, color="#333333", fontweight="bold", nudge_y=15)
    # Arrow showing drill path from Americas to breakdown
    + geom_segment(
        aes(x="x_start", xend="x_end", y="y_start", yend="y_end"),
        data=arrow_df,
        inherit_aes=False,
        color="#666666",
        size=1.5,
        linetype="dashed",
    )
    # Section labels
    + geom_text(
        aes(x="x", y="y", label="label"),
        data=section_labels,
        inherit_aes=False,
        size=14,
        color="#306998",
        fontweight="bold",
    )
    + scale_fill_manual(values=region_colors, name="Category")
    + scale_x_continuous(
        breaks=[0, 1, 2, 3, 5.5, 6.5, 7.5, 8.5],
        labels=["Americas", "Asia Pacific", "Europe", "MEA", "USA", "Canada", "Brazil", "Mexico"],
    )
    + scale_y_continuous(limits=(0, 900), expand=(0, 0))
    + labs(
        title="bar-drilldown · plotnine · pyplots.ai",
        subtitle="Static drilldown visualization: Click Americas (left) to see country breakdown (right)",
        x="",
        y="Sales ($ millions)",
    )
    + guides(fill=False)  # Hide legend since labels are on x-axis
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=26, weight="bold", color="#306998"),
        plot_subtitle=element_text(size=16, color="#666666"),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", alpha=0.4),
        panel_grid_minor=element_blank(),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
