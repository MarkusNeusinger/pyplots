"""
sparkline-basic: Basic Sparkline
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - simulated daily sales trend showing realistic variation
values = [
    42,
    45,
    48,
    44,
    52,
    58,
    55,
    61,
    59,
    63,
    68,
    65,
    72,
    70,
    75,
    73,
    78,
    82,
    79,
    85,
    88,
    84,
    91,
    87,
    95,
    92,
    98,
    96,
    102,
    105,
]

# Find min/max indices for highlighting
min_idx = values.index(min(values))
max_idx = values.index(max(values))

# Custom style for sparkline - minimal and clean
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),  # Python Blue for main line
    title_font_size=72,
    label_font_size=1,  # Minimize label size
    major_label_font_size=1,
    legend_font_size=48,
    value_font_size=1,
    stroke_width=6,  # Visible line at large canvas
    opacity=1.0,
    opacity_hover=1.0,
)

# Create sparkline chart - minimal configuration
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    show_x_labels=False,  # No X axis labels for sparkline
    show_y_labels=False,  # No Y axis labels for sparkline
    show_x_guides=False,  # No vertical gridlines
    show_y_guides=False,  # No horizontal gridlines
    show_legend=True,  # Show minimal legend with title
    legend_at_bottom=True,
    show_dots=False,  # Hide regular dots
    fill=True,  # Area fill for visual effect
    interpolate="cubic",  # Smooth line
    margin=100,
    title="sparkline-basic · pygal · pyplots.ai",
)

# Prepare data with highlighted min/max points
# Create main series with None placeholders for special points
main_data = [{"value": v, "color": "#306998"} for v in values]

# Highlight min point (Python Yellow)
main_data[min_idx] = {
    "value": values[min_idx],
    "color": "#FFD43B",
    "node": {"r": 20},  # Larger dot for visibility
}

# Highlight max point (Python Yellow)
main_data[max_idx] = {"value": values[max_idx], "color": "#FFD43B", "node": {"r": 20}}

# Highlight first and last points
main_data[0] = {"value": values[0], "color": "#306998", "node": {"r": 15}}
main_data[-1] = {"value": values[-1], "color": "#306998", "node": {"r": 15}}

chart.add("Daily Sales Trend", main_data, show_dots=True, dots_size=8)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
