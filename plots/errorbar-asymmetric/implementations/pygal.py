"""pyplots.ai
errorbar-asymmetric: Asymmetric Error Bars Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Data - Material strength testing (MPa) with asymmetric confidence intervals
materials = ["Steel", "Aluminum", "Titanium", "Copper", "Brass", "Bronze"]
# Central values (median strength)
y_values = [250, 150, 450, 200, 180, 220]
# Asymmetric errors - lower tends to be smaller (material won't suddenly get weaker)
# but upper can be higher (some samples exceed expected strength)
error_lower = [15, 12, 25, 10, 8, 12]  # 10th percentile distance from median
error_upper = [35, 28, 45, 22, 20, 30]  # 90th percentile distance from median

# Custom style for 4800x2700 canvas
# All error bars use the same color (#306998) for visual consistency
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#306998", "#306998", "#306998", "#306998", "#306998", "#306998"),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=36,
    stroke_width=6,
    opacity=1.0,
    transition="0s",
)

# Create XY chart for error bar visualization
# Each error bar will be a separate series to avoid connecting lines between bars
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="errorbar-asymmetric · pygal · pyplots.ai",
    x_title="Material",
    y_title="Tensile Strength (MPa)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
    show_y_guides=True,
    show_x_guides=False,
    print_values=False,
    margin=100,
    stroke=True,
    dots_size=20,
    range=(100, 550),
    xrange=(0, 7),
    x_labels=["", "Steel", "Aluminum", "Titanium", "Copper", "Brass", "Bronze"],
    x_labels_major_every=1,
    show_minor_x_labels=False,
)

# Add each error bar as a separate series (no legend entry for individual bars)
# This prevents lines connecting between different data points
# Add error bars first so central points appear on top
for i in range(len(materials)):
    x_pos = i + 1
    y_center = y_values[i]
    y_low = y_center - error_lower[i]
    y_high = y_center + error_upper[i]

    # Create vertical error bar segment
    bar_data = [(x_pos, y_low), (x_pos, y_high)]

    # Only first bar gets legend entry
    if i == 0:
        chart.add("10th-90th Percentile Range", bar_data, stroke=True, dots_size=10, stroke_style={"width": 6})
    else:
        chart.add(None, bar_data, stroke=True, dots_size=10, stroke_style={"width": 6})

# Add central points as main series (on top of error bars)
central_data = [(i + 1, y_values[i]) for i in range(len(materials))]
chart.add("Median Strength", central_data, stroke=False, dots_size=22)

# Render to files
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
