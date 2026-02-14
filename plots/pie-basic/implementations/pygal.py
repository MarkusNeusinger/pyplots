"""pyplots.ai
pie-basic: Basic Pie Chart
Library: pygal 3.1.0 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

import pygal
from pygal.style import Style


# Data - Global smartphone market share (2024)
companies = ["Apple", "Samsung", "Xiaomi", "OPPO", "vivo", "Others"]
share = [23.3, 19.4, 14.1, 8.7, 7.5, 27.0]

# Custom style for 3600x3600 px (square format)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#222",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3", "#A78BFA"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=56,
    value_font_size=48,
    tooltip_font_size=36,
    value_colors=("#FFFFFF", "#333333", "#FFFFFF", "#FFFFFF", "#333333", "#FFFFFF"),
)

# Create pie chart
chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    title="Smartphone Market Share · pie-basic · pygal · pyplots.ai",
    inner_radius=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=36,
    print_values=True,
    print_values_position="center",
    value_formatter=lambda x: f"{x:.1f}%",
    margin=40,
    margin_bottom=100,
)

# Add data with per-slice white stroke borders
for company, value in zip(companies, share, strict=True):
    chart.add(company, [{"value": value, "style": "stroke: white; stroke-width: 4"}])

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
