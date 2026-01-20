""" pyplots.ai
map-projections: World Map with Different Projections
Library: pygal 3.1.0 | Python 3.13.11
Quality: 86/100 | Created: 2026-01-20
"""

from pygal.style import Style
from pygal_maps_world.maps import World


# Pygal's world map uses a Robinson-like pseudo-cylindrical projection
# This visualization demonstrates how different projections distort areas
# by showing Mercator distortion factors (sec²(latitude)) for each country

# Mercator projection distortion factor by country latitude
# Values represent area scaling: 1.0 = true size, 14.0 = appears 14× larger
country_distortion = {
    # 60°-90° latitude: Extreme Mercator distortion (polar regions)
    "gl": 14.3,  # Greenland ~72°N
    "ru": 3.5,  # Russia ~61°N
    "ca": 3.0,  # Canada ~56°N
    "no": 2.8,  # Norway ~62°N
    "is": 2.6,  # Iceland ~65°N
    "se": 2.5,  # Sweden ~62°N
    "fi": 2.4,  # Finland ~64°N
    # 30°-60° latitude: High distortion (temperate zones)
    "us": 1.4,  # USA ~40°N
    "gb": 1.4,  # UK ~54°N
    "cl": 1.4,  # Chile ~35°S
    "de": 1.3,  # Germany ~51°N
    "fr": 1.3,  # France ~46°N
    "ar": 1.3,  # Argentina ~34°S
    "nz": 1.3,  # New Zealand ~41°S
    "jp": 1.2,  # Japan ~36°N
    "cn": 1.2,  # China ~35°N
    "au": 1.2,  # Australia ~25°S
    # 15°-30° latitude: Moderate distortion (subtropical)
    "za": 1.1,  # South Africa ~29°S
    "eg": 1.1,  # Egypt ~27°N
    "mx": 1.1,  # Mexico ~23°N
    # 0°-15° latitude: Minimal distortion (equatorial - Mercator accurate here)
    "br": 1.0,  # Brazil ~10°S
    "co": 1.0,  # Colombia ~4°N
    "ke": 1.0,  # Kenya ~0°
    "id": 1.0,  # Indonesia ~5°S
    "ng": 1.0,  # Nigeria ~10°N
    "cd": 1.0,  # DR Congo ~3°S
    "ec": 1.0,  # Ecuador ~0°
    "ug": 1.0,  # Uganda ~1°N
    "my": 1.0,  # Malaysia ~3°N
    "th": 1.0,  # Thailand ~15°N
    "vn": 1.0,  # Vietnam ~14°N
    "ph": 1.0,  # Philippines ~12°N
}

# Group countries by latitude bands (similar to graticule intervals)
# These bands correspond roughly to 30° latitude intervals
polar_zone = {k: v for k, v in country_distortion.items() if v >= 2.4}  # >60°
temperate_zone = {k: v for k, v in country_distortion.items() if 1.2 <= v < 2.4}  # 30-60°
subtropical_zone = {k: v for k, v in country_distortion.items() if 1.05 <= v < 1.2}  # 15-30°
equatorial_zone = {k: v for k, v in country_distortion.items() if v < 1.05}  # 0-15°

# Diverging color scheme: purple (high distortion) to green (low distortion)
colors = ("#762a83", "#c2a5cf", "#a6dba0", "#1b7837")

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=72,
    label_font_size=48,
    legend_font_size=44,
    major_label_font_size=44,
    value_font_size=40,
    tooltip_font_size=36,
    no_data_font_size=36,
)

# Create world map using pygal's built-in Robinson-style projection
worldmap = World(
    style=custom_style,
    width=4800,
    height=2700,
    title="map-projections · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=40,
    print_values=False,
    print_labels=False,
)

# Add data series by latitude zone - legend shows latitude bands like graticule
worldmap.add("60°+ latitude (distortion >2.4×)", polar_zone)
worldmap.add("30°-60° latitude (distortion 1.2-2.4×)", temperate_zone)
worldmap.add("15°-30° latitude (distortion 1.05-1.2×)", subtropical_zone)
worldmap.add("0°-15° latitude (distortion <1.05×)", equatorial_zone)

# Save outputs
worldmap.render_to_file("plot.html")
worldmap.render_to_png("plot.png")
