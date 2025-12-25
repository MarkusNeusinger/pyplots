""" pyplots.ai
pie-exploded: Exploded Pie Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-25
"""

import math

import pygal
from pygal.style import Style


# Data - Market share analysis highlighting the leader
categories = ["TechCorp", "DataFlow", "CloudBase", "NetSys", "Others"]
values = [35.2, 22.8, 18.5, 14.3, 9.2]
# Explosion distances (0 = no explosion, higher = more separation)
explode = [0.08, 0, 0.04, 0, 0]  # Explode leader and third place

# Custom style for large canvas (3600x3600 for pie chart)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95A5A6"),
    font_family="sans-serif",
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=32,
    tooltip_font_size=28,
)

# Calculate slice angles for explosion direction
total = sum(values)
angles = []
current_angle = -math.pi / 2  # Start at top (pygal starts at top)
for val in values:
    slice_angle = 2 * math.pi * (val / total)
    mid_angle = current_angle + slice_angle / 2
    angles.append(mid_angle)
    current_angle += slice_angle


def explode_slices(svg_tree):
    """Apply explode effect by translating pie slices outward from center."""
    # Base explosion distance (in pixels for 3600px canvas)
    base_distance = 80

    for elem in svg_tree.iter():
        if "class" in elem.attrib:
            cls = elem.attrib["class"]
            # Check for each serie
            for i, exp_dist in enumerate(explode):
                if f"serie-{i}" in cls and "series" in cls and exp_dist > 0:
                    # Calculate translation based on slice midpoint angle
                    angle = angles[i]
                    dx = math.cos(angle) * base_distance * (exp_dist / 0.1)
                    dy = math.sin(angle) * base_distance * (exp_dist / 0.1)

                    # Find and transform the slice path
                    for child in elem.iter():
                        if child.tag.endswith("path") and "slice" in child.attrib.get("class", ""):
                            child.set("transform", f"translate({dx:.1f}, {dy:.1f})")
    return svg_tree


# Create exploded pie chart (square format for pie)
chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    title="Market Share Analysis · pie-exploded · pygal · pyplots.ai",
    inner_radius=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=32,
    print_values=True,
    print_values_position="center",
    value_formatter=lambda x: f"{x:.1f}%",
    spacing=20,
)

# Add XML filter for explosion effect
chart.add_xml_filter(explode_slices)

# Add slices
for category, value in zip(categories, values, strict=True):
    chart.add(category, value)

# Save as PNG
chart.render_to_png("plot.png")

# Also save as HTML for interactivity
chart.render_to_file("plot.html")
