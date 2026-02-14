"""pyplots.ai
bar-basic: Basic Bar Chart
Library: pygal 3.1.0 | Python 3.14
Quality: 83/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data - Annual revenue by product category (sorted descending)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [58200, 37400, 24800, 15300, 9100, 4600]

# Highlight color for the leading category, muted for the rest
highlight_color = "#306998"
base_color = "#7FACC6"

# Build per-bar data with color emphasis on the leader
bar_data = [{"value": values[0], "color": highlight_color, "label": categories[0]}] + [
    {"value": v, "color": base_color} for v in values[1:]
]

# Custom style — refined for publication quality
custom_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#2C3E50",
    foreground_strong="#2C3E50",
    foreground_subtle="#D5D8DC",
    colors=(highlight_color,),
    title_font_size=52,
    label_font_size=38,
    major_label_font_size=38,
    value_font_size=36,
    value_label_font_size=36,
    legend_font_size=38,
    title_font_family="sans-serif",
    label_font_family="sans-serif",
    value_font_family="sans-serif",
)

# Create chart
chart = pygal.Bar(
    width=4800,
    height=2700,
    title="bar-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Revenue (USD)",
    style=custom_style,
    show_legend=False,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: f"${x:,.0f}",
    y_labels_major_every=2,
    show_y_guides=True,
    show_x_guides=False,
    margin=60,
    margin_bottom=80,
    spacing=25,
    rounded_bars=4,
    show_minor_y_labels=True,
    truncate_label=-1,
    x_label_rotation=0,
)

# Format y-axis labels with dollar signs
chart.y_labels = [0, 10000, 20000, 30000, 40000, 50000, 60000]

# Add data with per-bar styling
chart.x_labels = categories
chart.add("Revenue", bar_data)

# Save
chart.render_to_png("plot.png")
