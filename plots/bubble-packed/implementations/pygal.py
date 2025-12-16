"""
bubble-packed: Basic Packed Bubble Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Department budget allocation (values determine circle size)
data = {
    "Technology": [
        {"value": 450, "label": "Software Development"},
        {"value": 280, "label": "Cloud Infrastructure"},
        {"value": 180, "label": "Data Analytics"},
        {"value": 120, "label": "Security"},
    ],
    "Marketing": [
        {"value": 350, "label": "Digital Marketing"},
        {"value": 220, "label": "Brand & Creative"},
        {"value": 150, "label": "Events"},
        {"value": 90, "label": "PR"},
    ],
    "Operations": [
        {"value": 280, "label": "Facilities"},
        {"value": 200, "label": "HR & Recruiting"},
        {"value": 160, "label": "Legal"},
        {"value": 100, "label": "Admin"},
    ],
    "Sales": [
        {"value": 380, "label": "Enterprise"},
        {"value": 250, "label": "SMB"},
        {"value": 170, "label": "Partners"},
        {"value": 110, "label": "Support"},
    ],
}

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B"),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create treemap (best approximation of packed bubbles in pygal)
# Treemap shows hierarchical data by area, similar to packed bubble sizing
chart = pygal.Treemap(
    width=4800,
    height=2700,
    style=custom_style,
    title="Budget Allocation · bubble-packed · pygal · pyplots.ai",
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    print_values=True,
    value_formatter=lambda x: f"${x}K",
)

# Add data by category (groups)
for category, items in data.items():
    chart.add(category, items)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
