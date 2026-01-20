""" pyplots.ai
map-projections: World Map with Different Projections
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-20
"""

import numpy as np
from pygal.style import Style
from pygal_maps_world.maps import World


np.random.seed(42)

# Mercator projection distortion factor by country
# Higher values = more area distortion in Mercator projection
# Based on latitude: sec²(lat) scaling factor for areas near center latitude
country_distortion = {
    # High latitude - extreme Mercator distortion (appears much larger)
    "gl": 14.3,  # Greenland at ~72°N: appears 14× larger
    "ru": 3.5,  # Russia at ~61°N
    "ca": 3.0,  # Canada at ~56°N
    "no": 2.8,  # Norway at ~62°N
    "se": 2.5,  # Sweden at ~62°N
    "fi": 2.4,  # Finland at ~64°N
    "is": 2.6,  # Iceland at ~65°N
    # Mid latitude - moderate distortion
    "us": 1.4,  # USA at ~40°N
    "de": 1.3,  # Germany at ~51°N
    "fr": 1.3,  # France at ~46°N
    "gb": 1.4,  # UK at ~54°N
    "jp": 1.2,  # Japan at ~36°N
    "cn": 1.2,  # China at ~35°N
    "ar": 1.3,  # Argentina at ~34°S
    # Equatorial - minimal distortion (Mercator is accurate near equator)
    "br": 1.0,  # Brazil at ~10°S
    "co": 1.0,  # Colombia at ~4°N
    "ke": 1.0,  # Kenya at ~0°
    "id": 1.0,  # Indonesia at ~5°S
    "ng": 1.0,  # Nigeria at ~10°N
    "cd": 1.0,  # DR Congo at ~3°S
    "ec": 1.0,  # Ecuador at ~0°
    "ug": 1.0,  # Uganda at ~1°N
    "my": 1.0,  # Malaysia at ~3°N
    # Southern hemisphere mid-latitude
    "au": 1.2,  # Australia at ~25°S
    "za": 1.1,  # South Africa at ~29°S
    "nz": 1.3,  # New Zealand at ~41°S
    "cl": 1.4,  # Chile at ~35°S
}

# Group countries by distortion severity
extreme_distortion = {k: v for k, v in country_distortion.items() if v >= 2.4}
high_distortion = {k: v for k, v in country_distortion.items() if 1.3 <= v < 2.4}
moderate_distortion = {k: v for k, v in country_distortion.items() if 1.1 <= v < 1.3}
minimal_distortion = {k: v for k, v in country_distortion.items() if v < 1.1}

# Color palette: Red (extreme) → Orange → Yellow → Green (minimal distortion)
colors = ("#c51b7d", "#e9a3c9", "#a1d76a", "#4d9221")

# Custom style for large canvas with readable fonts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=72,
    label_font_size=48,
    legend_font_size=48,
    major_label_font_size=44,
    value_font_size=40,
    tooltip_font_size=36,
    no_data_font_size=36,
)

# Create world map (pygal uses Robinson-like pseudo-cylindrical projection)
# Title format: spec-id · library · pyplots.ai
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
    show_data_values=False,
)

# Add subtitle to explain the visualization
worldmap.x_title = "Robinson Projection showing Mercator Distortion Factor by Latitude"

# Add series by distortion level - legend shows what Mercator does to each region
worldmap.add("Extreme (≥2.4×): Polar regions", extreme_distortion)
worldmap.add("High (1.3-2.4×): Mid-latitude", high_distortion)
worldmap.add("Moderate (1.1-1.3×)", moderate_distortion)
worldmap.add("Minimal (<1.1×): Equatorial", minimal_distortion)

# Save outputs
worldmap.render_to_file("plot.html")
worldmap.render_to_png("plot.png")
