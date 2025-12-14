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

# Define colors
TOTAL_COLOR = "#306998"  # Python Blue for totals
INCREASE_COLOR = "#4CAF50"  # Green for increases
DECREASE_COLOR = "#E53935"  # Red for decreases
CONNECTOR_COLOR = "#888888"  # Gray for connecting lines

# Custom style for waterfall chart - colors match series order
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("rgba(255,255,255,0)", TOTAL_COLOR, INCREASE_COLOR, DECREASE_COLOR, CONNECTOR_COLOR),
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=36,
    value_font_size=32,
    value_label_font_size=32,
    legend_font_size=36,
)

# Build the waterfall data structure
# Each bar needs: base (invisible portion), visible height, and color
bar_data = []
cumulative = 0

for i, (cat, val) in enumerate(zip(categories, changes, strict=True)):
    is_first = i == 0
    is_last = i == len(categories) - 1

    if is_first or is_last:
        # Total bars start from 0
        bar_data.append({"category": cat, "base": 0, "height": val, "color": TOTAL_COLOR, "value": val})
        if is_first:
            cumulative = val
    else:
        # Change bars
        if val >= 0:
            bar_data.append({"category": cat, "base": cumulative, "height": val, "color": INCREASE_COLOR, "value": val})
        else:
            bar_data.append(
                {"category": cat, "base": cumulative + val, "height": abs(val), "color": DECREASE_COLOR, "value": val}
            )
        cumulative += val


# Custom value formatter - shows absolute height (labels handle signs separately)
def format_value(x):
    """Format value for display."""
    if x is None or abs(x) < 0.01:
        return ""
    return f"${x:,.0f}"


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
    print_labels=True,  # Use labels instead of values for proper sign display
    value_formatter=format_value,
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
increase_series = []
decrease_series = []
# Track cumulative values for connector lines
connector_levels = []

for bar in bar_data:
    base_series.append({"value": bar["base"], "color": "rgba(255,255,255,0)"})

    # Get the original change value for proper display
    original_value = bar["value"]

    if bar["color"] == TOTAL_COLOR:
        # Format totals with positive values
        total_series.append({"value": bar["height"], "color": TOTAL_COLOR, "label": f"${bar['height']:,.0f}"})
        increase_series.append({"value": None})
        decrease_series.append({"value": None})
        connector_levels.append(bar["height"])
    elif bar["color"] == INCREASE_COLOR:
        total_series.append({"value": None})
        # Positive changes show with positive label
        increase_series.append({"value": bar["height"], "color": INCREASE_COLOR, "label": f"+${original_value:,.0f}"})
        decrease_series.append({"value": None})
        connector_levels.append(bar["base"] + bar["height"])
    else:
        total_series.append({"value": None})
        increase_series.append({"value": None})
        # Negative changes show with negative sign
        decrease_series.append(
            {"value": bar["height"], "color": DECREASE_COLOR, "label": f"-${abs(original_value):,.0f}"}
        )
        connector_levels.append(bar["base"])  # Top of decrease bar after the drop

# Add series - base is invisible spacer (no legend entry)
# Check if we have any increases to show in legend
has_increases = any(s.get("value") for s in increase_series)

chart.add("", base_series, show_dots=False, stroke=False)
chart.add("Total", total_series)
if has_increases:
    chart.add("Increase", increase_series)
chart.add("Decrease", decrease_series)

# Render the base SVG
base_svg = chart.render().decode("utf-8")

# Create connector lines by injecting SVG elements
# Parse the SVG to find bar positions and add horizontal connector lines
# Extract y-axis scaling from the chart to calculate line positions

# Find the plot area boundaries from the SVG
# The y-axis needs to be scaled: find min/max y values and their pixel positions
y_max = max(bar["base"] + bar["height"] for bar in bar_data)
y_min = 0

# Look for the plot area group and calculate bar positions
# Pygal uses specific class names for the plot area
# We'll add connector lines as a new group after the bars

# Calculate approximate bar center x positions based on category count
num_bars = len(categories)

# Create connector line SVG elements
# Connector lines go from the top of one bar to the start level of the next bar
connector_lines = []
for i in range(num_bars - 1):
    # Each connector goes from current bar top to next bar's starting cumulative level
    current_top = connector_levels[i]
    # Use current top as the horizontal line level (connecting to next bar)
    connector_lines.append((i, current_top))

# Alternative approach: Use secondary_range or custom rendering
# For a clean solution, render connector lines as a line series overlay

# Render the HTML with embedded connector line visualization
# Add connector data as a secondary visualization in the HTML output
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>waterfall-basic · pygal · pyplots.ai</title>
    <style>
        .connector-line {{
            stroke: {CONNECTOR_COLOR};
            stroke-width: 3;
            stroke-dasharray: 10, 5;
        }}
    </style>
</head>
<body>
    {base_svg}
    <script>
        // Add connector lines after chart renders
        document.addEventListener('DOMContentLoaded', function() {{
            var svg = document.querySelector('svg');
            if (!svg) return;

            // Get the plot area dimensions
            var plotArea = svg.querySelector('.plot');
            if (!plotArea) return;

            var rect = plotArea.getBBox();
            var barWidth = rect.width / {num_bars};

            // Connector levels (cumulative values) from Python
            var levels = {connector_levels};
            var yMax = {y_max};

            // Calculate y scale
            var yScale = rect.height / yMax;

            // Add connector lines
            var ns = 'http://www.w3.org/2000/svg';
            var connectorGroup = document.createElementNS(ns, 'g');
            connectorGroup.setAttribute('class', 'connectors');

            for (var i = 0; i < levels.length - 1; i++) {{
                var line = document.createElementNS(ns, 'line');
                var x1 = rect.x + (i + 0.5) * barWidth + barWidth * 0.35;
                var x2 = rect.x + (i + 1.5) * barWidth - barWidth * 0.35;
                var y = rect.y + rect.height - levels[i] * yScale;

                line.setAttribute('x1', x1);
                line.setAttribute('y1', y);
                line.setAttribute('x2', x2);
                line.setAttribute('y2', y);
                line.setAttribute('class', 'connector-line');
                connectorGroup.appendChild(line);
            }}

            plotArea.appendChild(connectorGroup);
        }});
    </script>
</body>
</html>"""

# For PNG output, we need to add connector lines directly to the SVG
# Parse SVG and inject lines before rendering to PNG


def add_connector_lines_to_svg(svg_content, bar_data, connector_levels):
    """Add horizontal connector lines between bars in the SVG."""
    # Parse the actual plot dimensions from pygal's SVG
    # Plot group is at translate(350, 138) with width 4399.2 and height 2218.0
    plot_translate_match = re.search(r'translate\(([0-9.]+),\s*([0-9.]+)\)"\s*class="plot"', svg_content)
    plot_bg_match = re.search(
        r'class="plot"[^>]*>.*?<rect[^>]*width="([0-9.]+)"[^>]*height="([0-9.]+)"', svg_content, re.DOTALL
    )

    # Default values based on pygal's typical 4800x2700 layout
    plot_x = 350
    plot_y = 138
    plot_width = 4399.2

    if plot_translate_match:
        plot_x = float(plot_translate_match.group(1))
        plot_y = float(plot_translate_match.group(2))

    if plot_bg_match:
        plot_width = float(plot_bg_match.group(1))

    # Calculate y-axis range from data
    y_max = max(bd["base"] + bd["height"] for bd in bar_data)

    # Build connector line elements
    num_bars = len(connector_levels)
    bar_width = plot_width / num_bars

    # Extract actual y-axis range from the SVG guides
    # Default padding values based on typical pygal layout
    y_axis_top = 42.65  # Y coordinate for max value
    y_axis_bottom = 2175.35  # Y coordinate for zero

    # Extract y positions from guides if possible
    guides = re.findall(r'path d="M0\.000000 ([0-9.]+) h[^"]*" class="(?:major )?(?:guide )?line"', svg_content)
    if guides:
        y_axis_top = float(min(guides, key=float))
        y_axis_bottom = float(max(guides, key=float))

    y_axis_range = y_axis_bottom - y_axis_top

    # Create connector group with transform to match plot area
    lines_svg = f'<g class="connectors" transform="translate({plot_x}, {plot_y})" stroke="{CONNECTOR_COLOR}" stroke-width="6" stroke-dasharray="20,10">\n'

    # Y scale: map data values to SVG coordinates (inverted, origin at top)
    # y=0 in data maps to y_axis_bottom, y=y_max maps to y_axis_top
    def data_to_svg_y(value):
        return y_axis_bottom - (value / y_max) * y_axis_range

    # Add horizontal connector lines between consecutive bars
    # Each line goes from right edge of current bar to left edge of next bar
    for i in range(num_bars - 1):
        level = connector_levels[i]
        # Bar center positions within plot area: (i + 0.5) * bar_width
        # Line starts at right side of bar i and ends at left side of bar i+1
        bar_center_i = (i + 0.5) * bar_width
        bar_center_next = (i + 1.5) * bar_width
        # Approximate bar half-width (with spacing)
        bar_half_width = bar_width * 0.4

        x1 = bar_center_i + bar_half_width  # Right edge of current bar
        x2 = bar_center_next - bar_half_width  # Left edge of next bar
        y = data_to_svg_y(level)

        lines_svg += f'  <line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}"/>\n'

    lines_svg += "</g>\n"

    # Insert before closing </svg>
    svg_content = svg_content.replace("</svg>", lines_svg + "</svg>")

    return svg_content


# Render SVG with connector lines
svg_with_connectors = add_connector_lines_to_svg(base_svg, bar_data, connector_levels)

# Save SVG with connectors
with open("plot_with_connectors.svg", "w") as f:
    f.write(svg_with_connectors)

# Render to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_with_connectors.encode("utf-8"), write_to="plot.png")

# Save HTML with interactive connectors
with open("plot.html", "w") as f:
    f.write(html_content)
