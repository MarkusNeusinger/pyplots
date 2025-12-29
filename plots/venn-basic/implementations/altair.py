"""pyplots.ai
venn-basic: Venn Diagram
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-29
"""

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

# Circle parameters for 3-set Venn diagram with proper overlapping
# Using pixel coordinates for 1200x1200 canvas
radius = 200
# Position circles to overlap (closer together)
cx_a, cy_a = 500, 520  # A - left
cx_b, cy_b = 700, 520  # B - right
cx_c, cy_c = 600, 700  # C - bottom center

# Colors
colors = ["#306998", "#FFD43B", "#4DAF4A"]  # Python Blue, Python Yellow, Green

# Circle centers data
fill_centers = pd.DataFrame({"x": [cx_a, cx_b, cx_c], "y": [cy_a, cy_b, cy_c], "color": colors, "set": set_labels})

# Region counts with positions (in pixel coordinates for overlapping circles)
region_data = pd.DataFrame(
    {
        "x": [
            cx_a - 100,  # Only A (left side of A)
            cx_b + 100,  # Only B (right side of B)
            cx_c,  # Only C (bottom of C)
            (cx_a + cx_b) / 2,  # A ∩ B (top center)
            cx_a + 10,  # A ∩ C (left-bottom overlap)
            cx_b - 10,  # B ∩ C (right-bottom overlap)
            600,  # A ∩ B ∩ C (center of all three)
        ],
        "y": [
            cy_a,  # Only A
            cy_b,  # Only B
            cy_c + 100,  # Only C
            cy_a - 80,  # A ∩ B
            (cy_a + cy_c) / 2 + 30,  # A ∩ C
            (cy_b + cy_c) / 2 + 30,  # B ∩ C
            600,  # A ∩ B ∩ C
        ],
        "count": [str(only_a), str(only_b), str(only_c), str(only_ab), str(only_ac), str(only_bc), str(abc)],
    }
)

# Set name labels outside circles
set_label_data = pd.DataFrame(
    {"x": [cx_a - 170, cx_b + 170, cx_c], "y": [cy_a - 50, cy_b - 50, cy_c + 200], "label": set_labels}
)

# Calculate circle size for mark_point (size is area in pixels^2)
# We want circles with radius ~200 pixels visually
circle_size = radius * radius * 3.14

# Draw filled circles using point marks
background_circles = (
    alt.Chart(fill_centers)
    .mark_point(shape="circle", filled=True, opacity=0.35, size=circle_size)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        color=alt.Color("color:N", scale=None, legend=None),
    )
)

# Circle outlines
outline_circles = (
    alt.Chart(fill_centers)
    .mark_point(shape="circle", filled=False, strokeWidth=4, size=circle_size)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        stroke=alt.Color("color:N", scale=None, legend=None),
    )
)

# Region count labels
counts_layer = (
    alt.Chart(region_data)
    .mark_text(fontSize=24, fontWeight="bold", color="#1a1a1a")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        text="count:N",
    )
)

# Set name labels
names_layer = (
    alt.Chart(set_label_data)
    .mark_text(fontSize=22, fontWeight="bold", color="#333333")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[200, 1000]), axis=None),
        text="label:N",
    )
)

# Combine all layers
chart = (
    alt.layer(background_circles, outline_circles, counts_layer, names_layer)
    .properties(
        width=1200, height=1200, title=alt.Title(text="venn-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
