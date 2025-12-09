"""
area-stacked: Stacked Area Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Monthly revenue by product line over 2 years
months = [
    "Jan '23",
    "Feb '23",
    "Mar '23",
    "Apr '23",
    "May '23",
    "Jun '23",
    "Jul '23",
    "Aug '23",
    "Sep '23",
    "Oct '23",
    "Nov '23",
    "Dec '23",
    "Jan '24",
    "Feb '24",
    "Mar '24",
    "Apr '24",
    "May '24",
    "Jun '24",
    "Jul '24",
    "Aug '24",
    "Sep '24",
    "Oct '24",
    "Nov '24",
    "Dec '24",
]

# Revenue data for 4 product lines (in thousands)
electronics = [
    120,
    135,
    142,
    155,
    168,
    175,
    182,
    190,
    178,
    165,
    185,
    210,
    195,
    205,
    218,
    235,
    248,
    255,
    262,
    275,
    268,
    255,
    280,
    310,
]
clothing = [
    85,
    90,
    95,
    105,
    115,
    125,
    130,
    128,
    118,
    108,
    125,
    155,
    140,
    148,
    155,
    165,
    178,
    185,
    188,
    195,
    185,
    175,
    195,
    225,
]
home_garden = [45, 48, 55, 68, 85, 95, 98, 92, 78, 62, 55, 65, 58, 62, 72, 88, 105, 115, 118, 112, 95, 78, 72, 85]
sports = [35, 38, 42, 52, 65, 75, 82, 85, 72, 58, 48, 55, 48, 52, 58, 68, 82, 95, 102, 108, 92, 75, 65, 75]

# Custom style with pyplots color palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#DC2626", "#059669"),
    font_family="sans-serif",
    title_font_size=48,
    label_font_size=38,
    major_label_font_size=38,
    legend_font_size=38,
    opacity=0.75,
    opacity_hover=0.9,
)

# Create stacked area chart
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="Monthly Revenue by Product Line (2023-2024)",
    x_title="Month",
    y_title="Revenue ($ thousands)",
    style=custom_style,
    fill=True,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    legend_at_bottom=False,
    truncate_legend=-1,
    show_dots=False,
    stroke_style={"width": 2},
)

# Set x-axis labels
chart.x_labels = months

# Add data series (largest at bottom for stability)
chart.add("Electronics", electronics)
chart.add("Clothing", clothing)
chart.add("Home & Garden", home_garden)
chart.add("Sports", sports)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
