""" pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-16
"""

import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_bar,
    geom_text,
    ggplot,
    labs,
    position_stack,
    scale_fill_manual,
    theme,
    theme_minimal,
)


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
top_level_df["level"] = "1. All Regions"
top_level_df["display_name"] = top_level_df["name"]
top_level_df["sort_order"] = top_level_df["value"]

# Prepare data for drilled-down view (Americas breakdown)
drilled_df = df[df["parent"] == "americas"].copy()
drilled_df["level"] = "2. All > Americas"
drilled_df["display_name"] = drilled_df["name"]
drilled_df["sort_order"] = drilled_df["value"]

# Combine for faceted display
combined_df = pd.concat([top_level_df, drilled_df], ignore_index=True)

# Sort by value within each level for better visual
combined_df = combined_df.sort_values(["level", "sort_order"], ascending=[True, False])

# Define colors for each category
region_colors = {
    "Americas": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Asia Pacific": "#4B8BBE",  # Light Blue
    "MEA": "#E07B39",  # Orange
    # Drilled countries (Americas shades)
    "USA": "#306998",
    "Canada": "#4B8BBE",
    "Brazil": "#5A9BD4",
    "Mexico": "#7FB3D5",
}

# Set ordered category for x-axis to respect sort order
for lvl in combined_df["level"].unique():
    mask = combined_df["level"] == lvl
    order = combined_df.loc[mask, "display_name"].tolist()
    combined_df.loc[mask, "display_name"] = pd.Categorical(
        combined_df.loc[mask, "display_name"], categories=order, ordered=True
    )

# Create the plot
plot = (
    ggplot(combined_df, aes(x="display_name", y="value", fill="name"))
    + geom_bar(stat="identity", width=0.7, show_legend=False)
    + geom_text(aes(label="value"), position=position_stack(vjust=1.05), size=11, color="#333333", fontweight="bold")
    + facet_wrap("~level", scales="free_x", ncol=2)
    + scale_fill_manual(values=region_colors)
    + labs(
        title="bar-drilldown · plotnine · pyplots.ai",
        subtitle="Static drilldown: Top-level regions (left) and Americas breakdown (right)",
        x="",
        y="Sales ($ millions)",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold", color="#306998"),
        plot_subtitle=element_text(size=14, color="#666666"),
        axis_title_y=element_text(size=18),
        axis_text_x=element_text(size=14, angle=0),
        axis_text_y=element_text(size=14),
        strip_text=element_text(size=16, weight="bold"),
        strip_background=element_rect(fill="#f0f0f0", color="none"),
        panel_grid_major_x=element_line(alpha=0),
        panel_grid_major_y=element_line(color="#cccccc", alpha=0.5),
        panel_grid_minor=element_line(alpha=0),
        panel_spacing=0.4,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
