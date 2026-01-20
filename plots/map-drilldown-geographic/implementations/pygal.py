""" pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-20
"""

from pygal.style import Style
from pygal_maps_world.maps import World


# Hierarchical sales data - country-level values grouped by region
# This simulates drill-down from region to country level
country_sales = {
    # Europe
    "de": 580,
    "fr": 520,
    "gb": 490,
    "it": 380,
    "es": 290,
    "nl": 190,
    # Asia
    "cn": 1200,
    "jp": 850,
    "in": 420,
    "kr": 380,
    "sg": 180,
    "th": 170,
    # North America
    "us": 2100,
    "ca": 480,
    "mx": 220,
    # South America
    "br": 520,
    "ar": 180,
    "cl": 120,
    "co": 70,
    # Africa
    "za": 280,
    "eg": 150,
    "ng": 110,
    "ke": 80,
    # Oceania
    "au": 380,
    "nz": 70,
}

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#FF6B6B", "#4ECDC4", "#95E1A3"),
    title_font_size=64,
    label_font_size=40,
    legend_font_size=36,
    major_label_font_size=36,
    value_font_size=32,
    tooltip_font_size=32,
    no_data_font_size=28,
)

# Create world map with country-level drill-down data
# The interactive HTML allows clicking countries to see detailed values
# Breadcrumb: World > [Click any region to drill down]
worldmap = World(
    style=custom_style,
    width=4800,
    height=2700,
    title="map-drilldown-geographic \u00b7 pygal \u00b7 pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=36,
    print_values=False,
    print_labels=False,
)

# Group countries by sales performance tier for choropleth coloring
# This creates visual hierarchy to guide drill-down exploration
tier1 = {k: v for k, v in country_sales.items() if v >= 500}  # High performers
tier2 = {k: v for k, v in country_sales.items() if 200 <= v < 500}  # Medium
tier3 = {k: v for k, v in country_sales.items() if 100 <= v < 200}  # Low-medium
tier4 = {k: v for k, v in country_sales.items() if v < 100}  # Emerging

# Add data series - each tier clickable for drill-down detail
worldmap.add("Sales $500M+ (click to drill)", tier1)
worldmap.add("Sales $200-500M (click to drill)", tier2)
worldmap.add("Sales $100-200M (click to drill)", tier3)
worldmap.add("Sales <$100M (click to drill)", tier4)

# Save interactive HTML with drill-down tooltips
# Hover over any country to see exact sales value
worldmap.render_to_file("plot.html")
worldmap.render_to_png("plot.png")
