"""pyplots.ai
waterfall-basic: Basic Waterfall Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import pygal
from pygal.style import Style


# Data: Quarterly financial breakdown from revenue to net income
categories = ["Q1 Revenue", "Product Sales", "Services", "COGS", "Operating Exp", "Other Income", "Taxes", "Net Income"]
changes = [500, 150, 80, -180, -120, 25, -68, None]  # None for the final total

# Calculate running totals and positions for waterfall effect
running_total = 0
bar_bottoms = []
bar_heights = []
bar_types = []  # 'total', 'positive', 'negative'
display_values = []  # Values to display on bars

for i, val in enumerate(changes):
    if i == 0:
        # Starting total
        bar_bottoms.append(0)
        bar_heights.append(val)
        bar_types.append("total")
        display_values.append(val)
        running_total = val
    elif val is None:
        # Final total - calculate from running total
        bar_bottoms.append(0)
        bar_heights.append(running_total)
        bar_types.append("total")
        display_values.append(running_total)
    elif val >= 0:
        # Positive change
        bar_bottoms.append(running_total)
        bar_heights.append(val)
        bar_types.append("positive")
        display_values.append(val)
        running_total += val
    else:
        # Negative change
        running_total += val
        bar_bottoms.append(running_total)
        bar_heights.append(abs(val))
        bar_types.append("negative")
        display_values.append(val)

# Custom style for large canvas with filled bars
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("transparent", "#306998", "#2E7D32", "#C62828"),  # spacer, total, positive, negative
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=28,
    value_colors=("transparent", "#333333", "#333333", "#333333"),
    opacity=1.0,
    opacity_hover=0.9,
)

# Create stacked bar chart
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="waterfall-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Amount ($K)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=24,
    show_y_guides=True,
    show_x_guides=False,
    print_values=False,
    truncate_legend=-1,
    truncate_label=-1,
    x_label_rotation=0,
    margin=80,
    margin_bottom=150,
    spacing=40,
)

# Set x-axis labels
chart.x_labels = categories

# Separate data by type for coloring
spacer_data = []
total_data = []
positive_data = []
negative_data = []

for i in range(len(categories)):
    bottom = bar_bottoms[i]
    height = bar_heights[i]
    btype = bar_types[i]
    disp_val = display_values[i]

    # Spacer to create floating effect
    spacer_data.append({"value": bottom, "label": ""})

    if btype == "total":
        total_data.append({"value": height, "label": f"{disp_val}"})
        positive_data.append(None)
        negative_data.append(None)
    elif btype == "positive":
        total_data.append(None)
        positive_data.append({"value": height, "label": f"+{disp_val}"})
        negative_data.append(None)
    else:
        total_data.append(None)
        positive_data.append(None)
        negative_data.append({"value": height, "label": f"{disp_val}"})

# Add series in stack order (bottom to top)
# The spacer creates the floating effect - use stroke_style to hide it
chart.add("", spacer_data, stroke_style={"width": 0})  # Invisible spacer
chart.add("Total", total_data)
chart.add("Increase", positive_data)
chart.add("Decrease", negative_data)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
