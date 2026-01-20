""" pyplots.ai
map-projections: World Map with Different Projections
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-20
"""

import numpy as np
from pygal.style import Style
from pygal_maps_world.maps import World


# Data: Highlighting regions to show projection distortion effects
# Areas that appear distorted in Mercator projection vs reality
np.random.seed(42)

# Country codes with relative size distortion in Mercator projection
# (Positive = appears larger than actual, Negative = appears smaller)
# Values represent approximate distortion factor at country's latitude
country_distortion = {
    # High latitude (extreme distortion in Mercator)
    "gl": 14.3,  # Greenland - appears 14x larger
    "ru": 3.5,  # Russia
    "ca": 3.0,  # Canada
    "no": 2.8,  # Norway
    "se": 2.5,  # Sweden
    "fi": 2.4,  # Finland
    # Mid latitude (moderate distortion)
    "us": 1.3,
    "de": 1.2,
    "fr": 1.2,
    "gb": 1.2,
    "jp": 1.2,
    # Equatorial (minimal distortion)
    "br": 1.0,
    "co": 1.0,
    "ke": 1.0,
    "id": 1.0,
    "ng": 1.0,
    "cd": 1.0,  # DR Congo
    # Southern hemisphere mid-latitude
    "au": 1.2,
    "ar": 1.3,
    "za": 1.1,
    "nz": 1.2,
    "cl": 1.3,
}

# Group countries by distortion level for legend
extreme_distortion = {k: v for k, v in country_distortion.items() if v >= 2.5}
high_distortion = {k: v for k, v in country_distortion.items() if 1.3 <= v < 2.5}
moderate_distortion = {k: v for k, v in country_distortion.items() if 1.1 <= v < 1.3}
minimal_distortion = {k: v for k, v in country_distortion.items() if v < 1.1}

# Color palette showing distortion intensity
# Red/orange = extreme distortion (high latitude), Green = accurate (equator)
colors = ("#d73027", "#fc8d59", "#fee08b", "#1a9850")

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=72,
    label_font_size=44,
    legend_font_size=44,
    major_label_font_size=40,
    value_font_size=36,
    tooltip_font_size=32,
    no_data_font_size=32,
)

# Create world map showing Mercator distortion effects
# (The built-in map uses Robinson-like projection, itself relatively accurate)
worldmap = World(
    style=custom_style,
    width=4800,
    height=2700,
    title="Mercator Projection Distortion · map-projections · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=36,
)

# Add series showing distortion levels (what Mercator would show vs actual)
worldmap.add("Extreme (>2.5x)", extreme_distortion)
worldmap.add("High (1.3-2.5x)", high_distortion)
worldmap.add("Moderate (1.1-1.3x)", moderate_distortion)
worldmap.add("Minimal (<1.1x)", minimal_distortion)

# Save outputs
worldmap.render_to_file("plot.html")
worldmap.render_to_png("plot.png")
