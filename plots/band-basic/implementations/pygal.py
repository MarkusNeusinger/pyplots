"""
band-basic: Basic Band Plot
Library: pygal
"""

import re

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.arange(0, 50)

# Create central trend line (simulating a model prediction)
y_center = 50 + 0.8 * x + 5 * np.sin(x / 5)

# Create upper and lower bounds (confidence interval)
uncertainty = 3 + 0.5 * np.sqrt(x)  # Increasing uncertainty over time
y_upper = y_center + uncertainty
y_lower = y_center - uncertainty

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    # Colors: transparent base, band fill (blue with alpha)
    colors=("rgba(255,255,255,0)", "rgba(48,105,152,0.35)"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

# Create stacked line chart to simulate band
# pygal doesn't have native band support, so we use stacking technique:
# 1. Transparent base at y_lower level
# 2. Band fill (y_upper - y_lower) stacked on top
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="band-basic · pygal · pyplots.ai",
    x_title="Time (units)",
    y_title="Value",
    style=custom_style,
    fill=True,
    show_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    legend_at_bottom=True,
    truncate_legend=-1,
    range=(min(y_lower) - 5, max(y_upper) + 5),
    show_legend=True,
)

# X-axis labels (show every 10th for readability)
chart.x_labels = [str(int(v)) if v % 10 == 0 else "" for v in x]

# Add lower boundary as transparent base (blends with white background)
chart.add(None, [float(v) for v in y_lower], fill=True, stroke=False)

# Add band height (stacks on top of base to reach y_upper)
band_height = y_upper - y_lower
chart.add("95% Confidence Interval", [float(v) for v in band_height], fill=True, stroke=False)

# Create separate Line chart for central trend line with identical axes
# This will be rendered as SVG and combined with the band chart
line_style = Style(
    background="transparent",
    plot_background="transparent",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#FFD43B",),  # Python yellow for center line
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

line_chart = pygal.Line(
    width=4800,
    height=2700,
    style=line_style,
    fill=False,
    show_dots=False,
    show_y_guides=False,
    show_x_guides=False,
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    show_minor_y_labels=False,
    print_values=False,
    range=(min(y_lower) - 5, max(y_upper) + 5),
    stroke_style={"width": 6},
    title="",
    x_title="",
    y_title="",
)

# Match x-axis with main chart
line_chart.x_labels = [str(int(v)) for v in x]

# Add central trend line data
line_chart.add("Central Trend", [float(v) for v in y_center])

# Render both charts to SVG and combine them
band_svg = chart.render().decode("utf-8")
line_svg = line_chart.render().decode("utf-8")

# Extract the plot group from line chart (contains the trend line path)
# Find the series group in line SVG
series_match = re.search(r'(<g class="series serie-0[^"]*".*?</g>)', line_svg, re.DOTALL)

if series_match:
    line_series = series_match.group(1)
    # Modify the line to have proper styling
    line_series = line_series.replace('class="line ', 'class="line center-line ')
    # Add stroke-width inline for the path
    line_series = re.sub(
        r'(<path[^>]*class="line[^"]*")', r'\1 style="stroke:#FFD43B;stroke-width:6;fill:none"', line_series
    )

    # Find where to insert in band SVG (after the last series group)
    # Insert before the closing </svg> but after all series
    insert_pos = band_svg.rfind("</svg>")
    if insert_pos > 0:
        # Find the existing legends group and add the center line legend
        # Look for the legends group closing tag
        legends_match = re.search(
            r'(<g transform="translate\([^)]+\)" class="legends">.*?)(</g>\s*</g>)', band_svg, re.DOTALL
        )
        if legends_match:
            # Insert additional legend entry before the closing of legends group
            legend_entry = """<g id="activate-serie-2" class="legend reactive activate-serie" transform="translate(400, 0)"><rect x="0.0" y="15.0" width="12" height="12" style="fill:#FFD43B" class="reactive" /><text x="17.0" y="33.6">Central Trend</text></g>"""

            # Find position right before the last </g> of the legends group
            legends_end = band_svg.find("</g></g>", legends_match.start())
            if legends_end > 0:
                combined_svg = band_svg[:legends_end] + legend_entry + band_svg[legends_end:]
                # Now insert the line series before </svg>
                insert_pos = combined_svg.rfind("</svg>")
                combined_svg = combined_svg[:insert_pos] + line_series + combined_svg[insert_pos:]
            else:
                combined_svg = band_svg[:insert_pos] + line_series + band_svg[insert_pos:]
        else:
            combined_svg = band_svg[:insert_pos] + line_series + band_svg[insert_pos:]
    else:
        combined_svg = band_svg
else:
    combined_svg = band_svg

# Save as HTML (SVG)
with open("plot.html", "w") as f:
    f.write(combined_svg)

# Save as PNG using cairosvg
cairosvg.svg2png(bytestring=combined_svg.encode("utf-8"), write_to="plot.png")
