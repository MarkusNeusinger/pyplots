"""
waterfall-basic: Basic Waterfall Chart
Library: pygal
"""

import re

import cairosvg
import pygal
from pygal.style import Style


# Data - Quarterly financial breakdown from revenue to net income
categories = ["Revenue", "Cost of Sales", "Operating Exp", "Taxes", "Net Income"]
changes = [150000, -45000, -35000, -22000, None]  # None = final total

# Calculate running total for the final value
running_total = sum(c for c in changes[:-1] if c is not None)
changes[-1] = running_total  # Set final total

# Define colorblind-safe colors (avoid red-green)
TOTAL_COLOR = "#306998"  # Python Blue for totals
INCREASE_COLOR = "#306998"  # Python Blue for increases (same as totals for this data)
DECREASE_COLOR = "#FF9800"  # Orange for decreases (colorblind-safe)
CONNECTOR_COLOR = "#666666"  # Gray for connecting lines

# Custom style for waterfall chart
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("rgba(255,255,255,0)", TOTAL_COLOR, DECREASE_COLOR),
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=36,
    value_font_size=32,
    value_label_font_size=32,
    legend_font_size=36,
    guide_stroke_color="#cccccc",
    major_guide_stroke_color="#999999",
)

# Build the waterfall data structure
# Each bar needs: base (invisible portion), visible height, and type
bar_data = []
cumulative = 0

for i, (cat, val) in enumerate(zip(categories, changes, strict=True)):
    is_first = i == 0
    is_last = i == len(categories) - 1

    if is_first or is_last:
        # Total bars start from 0
        bar_data.append({"category": cat, "base": 0, "height": val, "type": "total", "value": val})
        if is_first:
            cumulative = val
    else:
        # Change bars - negative values stack downward from cumulative
        if val >= 0:
            bar_data.append({"category": cat, "base": cumulative, "height": val, "type": "increase", "value": val})
        else:
            bar_data.append(
                {"category": cat, "base": cumulative + val, "height": abs(val), "type": "decrease", "value": val}
            )
        cumulative += val

# Create a stacked bar chart - first stack is invisible base, second is visible bar
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    title="waterfall-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Amount ($)",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    print_values=False,
    print_labels=True,
    show_y_guides=True,
    show_x_guides=False,
    margin=50,
    spacing=40,
)

# Set x labels
chart.x_labels = categories

# Create the base (invisible) series and colored bar series
base_series = []
total_series = []
decrease_series = []

# Track cumulative values for connector lines
connector_levels = []

for bar in bar_data:
    base_series.append({"value": bar["base"], "color": "rgba(255,255,255,0)"})

    if bar["type"] == "total":
        # Format totals with positive values
        total_series.append({"value": bar["height"], "color": TOTAL_COLOR, "label": f"${bar['height']:,.0f}"})
        decrease_series.append({"value": None})
        connector_levels.append(bar["height"])
    else:
        # This is a decrease (all intermediate bars in this data are decreases)
        total_series.append({"value": None})
        decrease_series.append(
            {"value": bar["height"], "color": DECREASE_COLOR, "label": f"-${abs(bar['value']):,.0f}"}
        )
        connector_levels.append(bar["base"])

# Add series - base is invisible spacer
chart.add("", base_series, show_dots=False, stroke=False)
chart.add("Total", total_series)
chart.add("Decrease", decrease_series)

# Render base SVG
base_svg = chart.render().decode("utf-8")

# Add connector lines directly in SVG
# Pygal uses a plot area with transform - parse the SVG to find dimensions
# Plot area is typically at translate(X, Y) with the plot background rect

# Find plot transform: translate(X, Y)
plot_match = re.search(r'transform="translate\(([0-9.]+),\s*([0-9.]+)\)"[^>]*class="plot"', base_svg)
plot_x = float(plot_match.group(1)) if plot_match else 350.0
plot_y = float(plot_match.group(2)) if plot_match else 138.0

# Find plot dimensions from the background rect inside plot group
bg_match = re.search(
    r'class="plot"[^>]*>.*?<rect class="background"[^>]*width="([0-9.]+)"[^>]*height="([0-9.]+)"', base_svg, re.DOTALL
)
plot_width = float(bg_match.group(1)) if bg_match else 4399.2
plot_height = float(bg_match.group(2)) if bg_match else 2132.7

# Y-axis range from data
y_max = max(bd["base"] + bd["height"] for bd in bar_data)
y_min = 0

# Extract y positions from guide lines to get accurate scaling
guides = re.findall(r'path d="M0\.000000 ([0-9.]+) h[0-9.]+" class="[^"]*guide[^"]*line"', base_svg)
if guides:
    y_axis_top = float(min(guides, key=float))
    y_axis_bottom = float(max(guides, key=float))
else:
    # Default based on typical pygal layout with margins
    y_axis_top = 42.65
    y_axis_bottom = plot_height - 42.65

y_axis_range = y_axis_bottom - y_axis_top

# Build connector lines SVG group
num_bars = len(connector_levels)
bar_width = plot_width / num_bars

connector_lines = f'<g class="connectors" transform="translate({plot_x}, {plot_y})" stroke="{CONNECTOR_COLOR}" stroke-width="6" stroke-dasharray="20,10">\n'

for i in range(num_bars - 1):
    level = connector_levels[i]
    # Map data value to SVG y coordinate (inverted - 0 at bottom)
    y = y_axis_bottom - (level / y_max) * y_axis_range

    # Horizontal line from right edge of bar i to left edge of bar i+1
    bar_center_i = (i + 0.5) * bar_width
    bar_center_next = (i + 1.5) * bar_width
    bar_half_width = bar_width * 0.35  # Leave gap from bar edges

    x1 = bar_center_i + bar_half_width
    x2 = bar_center_next - bar_half_width

    connector_lines += f'  <line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}"/>\n'

connector_lines += "</g>\n"

# Insert connector lines before closing </svg>
svg_with_connectors = base_svg.replace("</svg>", connector_lines + "</svg>")

# Save SVG
with open("plot.svg", "w") as f:
    f.write(svg_with_connectors)

# Render to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_with_connectors.encode("utf-8"), write_to="plot.png")

# HTML with embedded SVG
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>waterfall-basic · pygal · pyplots.ai</title>
</head>
<body>
    {svg_with_connectors}
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
