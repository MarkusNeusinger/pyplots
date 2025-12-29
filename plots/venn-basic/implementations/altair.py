""" pyplots.ai
venn-basic: Venn Diagram
Library: altair 6.0.0 | Python 3.13.11
Quality: 86/100 | Created: 2025-12-29
"""

import math

import altair as alt
import pandas as pd


# Data - Three overlapping research disciplines
set_labels = ["Machine Learning", "Statistics", "Data Engineering"]
set_sizes = [100, 80, 60]
# Overlaps: AB=30, AC=20, BC=25, ABC=10
only_a = 100 - 30 - 20 + 10  # 60
only_b = 80 - 30 - 25 + 10  # 35
only_c = 60 - 20 - 25 + 10  # 25
only_ab = 30 - 10  # 20
only_ac = 20 - 10  # 10
only_bc = 25 - 10  # 15
abc = 10

# Calculate proportional radii based on set sizes
# Base radius scaled so circles fill canvas well (centered at 600,600 in 1200x1200)
base_radius = 220
radius_a = base_radius * math.sqrt(set_sizes[0] / 100)  # 220 (100 -> 1.0)
radius_b = base_radius * math.sqrt(set_sizes[1] / 100)  # ~197 (80 -> 0.894)
radius_c = base_radius * math.sqrt(set_sizes[2] / 100)  # ~170 (60 -> 0.775)

# Position circles centered in canvas with proper overlap
# A (left-top), B (right-top), C (bottom-center)
center_x, center_y = 600, 600  # True center of canvas
offset_x = 130  # Horizontal offset for A and B from center
offset_y_top = -70  # Vertical offset for A and B (above center)
offset_y_bottom = 120  # Vertical offset for C (below center)

cx_a, cy_a = center_x - offset_x, center_y + offset_y_top  # A - left-top
cx_b, cy_b = center_x + offset_x, center_y + offset_y_top  # B - right-top
cx_c, cy_c = center_x, center_y + offset_y_bottom  # C - bottom-center

# Colors
colors = ["#306998", "#FFD43B", "#4DAF4A"]  # Python Blue, Python Yellow, Green

# Circle sizes for mark_point (proportional to set sizes)
circle_size_a = radius_a * radius_a * 3.14
circle_size_b = radius_b * radius_b * 3.14
circle_size_c = radius_c * radius_c * 3.14

# Circle centers data with individual sizes
fill_centers = pd.DataFrame(
    {
        "x": [cx_a, cx_b, cx_c],
        "y": [cy_a, cy_b, cy_c],
        "color": colors,
        "set": set_labels,
        "size": [circle_size_a, circle_size_b, circle_size_c],
    }
)

# Region counts with positions - adjusted for better centered layout
region_data = pd.DataFrame(
    {
        "x": [
            cx_a - 90,  # Only A (left side of A)
            cx_b + 90,  # Only B (right side of B)
            cx_c,  # Only C (bottom of C)
            center_x,  # A ∩ B (between A and B)
            cx_a + 60,  # A ∩ C (overlap of A and C)
            cx_b - 60,  # B ∩ C (overlap of B and C)
            center_x,  # A ∩ B ∩ C (center of all three)
        ],
        "y": [
            cy_a - 20,  # Only A
            cy_b - 20,  # Only B
            cy_c + 90,  # Only C
            cy_a - 70,  # A ∩ B
            (cy_a + cy_c) / 2 + 40,  # A ∩ C
            (cy_b + cy_c) / 2 + 40,  # B ∩ C
            center_y + 20,  # A ∩ B ∩ C
        ],
        "count": [str(only_a), str(only_b), str(only_c), str(only_ab), str(only_ac), str(only_bc), str(abc)],
    }
)

# Set name labels outside circles - positioned prominently for visibility
set_label_data = pd.DataFrame(
    {"x": [cx_a - 200, cx_b + 200, cx_c], "y": [cy_a - 130, cy_b - 130, cy_c + 200], "label": set_labels}
)

# Draw filled circles using point marks with proportional sizes
background_circles = (
    alt.Chart(fill_centers)
    .mark_point(shape="circle", filled=True, opacity=0.35)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        color=alt.Color("color:N", scale=None, legend=None),
        size=alt.Size("size:Q", scale=None, legend=None),
    )
)

# Circle outlines with proportional sizes
outline_circles = (
    alt.Chart(fill_centers)
    .mark_point(shape="circle", filled=False, strokeWidth=4)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        stroke=alt.Color("color:N", scale=None, legend=None),
        size=alt.Size("size:Q", scale=None, legend=None),
    )
)

# Region count labels - larger font for better legibility at 3600x3600
counts_layer = (
    alt.Chart(region_data)
    .mark_text(fontSize=42, fontWeight="bold", color="#1a1a1a")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        text="count:N",
    )
)

# Set name labels - larger font for better legibility at 3600x3600
names_layer = (
    alt.Chart(set_label_data)
    .mark_text(fontSize=36, fontWeight="bold", color="#333333")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[100, 1100]), axis=None),
        text="label:N",
    )
)

# Combine all layers
chart = (
    alt.layer(background_circles, outline_circles, counts_layer, names_layer)
    .properties(
        width=1200, height=1200, title=alt.Title(text="venn-basic · altair · pyplots.ai", fontSize=40, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
