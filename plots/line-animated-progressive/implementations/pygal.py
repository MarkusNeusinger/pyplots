""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: pygal 3.1.0 | Python 3.13.11
Quality: 90/100 | Created: 2026-01-07
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - Monthly website traffic over 12 months
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base_traffic = 50000
trend = np.linspace(0, 30000, 12)
seasonal = 5000 * np.sin(np.linspace(0, 2 * np.pi, 12))
noise = np.random.normal(0, 2000, 12)
visitors = base_traffic + trend + seasonal + noise
visitors = np.maximum(visitors, 10000).astype(int)

# Fixed y-axis range for all panels (ensures visual consistency)
y_min = int(min(visitors) * 0.9)
y_max = int(max(visitors) * 1.1)

# Panel dimensions
panel_width = 2300
panel_height = 1200

# Style with highlight color for the trailing point
highlight_color = "#FF6B35"  # Orange highlight for current point
base_color = "#306998"  # Python blue for main line

# Stage configurations: (title, subtitle, num_points)
stages = [
    ("Stage 1: Q1 Data", "January - March", 3),
    ("Stage 2: H1 Data", "January - June", 6),
    ("Stage 3: 9 Months", "January - September", 9),
    ("Stage 4: Full Year", "January - December", 12),
]

panels = []
for title, subtitle, n_points in stages:
    # Style with two colors: base color for line, highlight for trailing point
    panel_style = Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=(base_color, highlight_color),
        font_family="sans-serif",
        title_font_size=56,
        label_font_size=36,
        major_label_font_size=36,
        legend_font_size=36,
        value_font_size=32,
        stroke_width=8,
        opacity=0.9,
    )

    chart = pygal.Line(
        title=title,
        x_title=subtitle,
        y_title="Visitors",
        width=panel_width,
        height=panel_height,
        style=panel_style,
        show_x_guides=False,
        show_y_guides=True,
        show_dots=True,
        dots_size=14,
        stroke_style={"width": 8, "linecap": "round", "linejoin": "round"},
        fill=False,
        show_legend=False,
        margin=60,
        spacing=40,
        x_label_rotation=0,
        print_values=False,
        interpolate="cubic",
        range=(y_min, y_max),
    )
    chart.x_labels = months

    # Main line series (all points except the last visible one)
    main_data = list(visitors[: n_points - 1]) + [None] * (13 - n_points)
    chart.add("Traffic", main_data)

    # Highlight series: just the last two points to show continuation with highlight
    highlight_data = [None] * (n_points - 2) + list(visitors[n_points - 2 : n_points]) + [None] * (12 - n_points)
    chart.add("Current", highlight_data)

    panels.append(Image.open(io.BytesIO(chart.render_to_png())))

# Create small multiples layout (2x2 grid)
margin = 100
title_height = 150
final_width = 4800
final_height = 2700
final_image = Image.new("RGB", (final_width, final_height), "white")

# Calculate panel positions to center the grid
grid_width = 2 * panel_width + margin
grid_height = 2 * panel_height + margin
x_offset = (final_width - grid_width) // 2
y_offset = title_height + (final_height - title_height - grid_height) // 2

# Paste panels in 2x2 grid
positions = [
    (x_offset, y_offset),  # Top-left: Stage 1
    (x_offset + panel_width + margin, y_offset),  # Top-right: Stage 2
    (x_offset, y_offset + panel_height + margin),  # Bottom-left: Stage 3
    (x_offset + panel_width + margin, y_offset + panel_height + margin),  # Bottom-right: Stage 4
]
for panel, pos in zip(panels, positions, strict=True):
    final_image.paste(panel, pos)

# Add title at top center
draw = ImageDraw.Draw(final_image)
title_text = "line-animated-progressive · pygal · pyplots.ai"
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 72)
except OSError:
    font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), title_text, font=font)
text_width = bbox[2] - bbox[0]
text_x = (final_width - text_width) // 2
draw.text((text_x, 40), title_text, fill="#333333", font=font)

# Save PNG output
final_image.save("plot.png", dpi=(300, 300))

# Generate interactive HTML with progressive series overlay
html_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(base_color, "#5A9BD5", "#70AD47", highlight_color),
    font_family="sans-serif",
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=40,
    stroke_width=8,
    opacity=0.85,
    opacity_hover=1.0,
    transition="500ms ease-in-out",
)

html_chart = pygal.Line(
    width=4800,
    height=2700,
    style=html_style,
    title="line-animated-progressive · pygal · pyplots.ai",
    x_title="Month",
    y_title="Website Visitors",
    show_x_guides=False,
    show_y_guides=True,
    show_dots=True,
    dots_size=16,
    stroke_style={"width": 8, "linecap": "round", "linejoin": "round"},
    fill=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    truncate_legend=-1,
    margin=80,
    spacing=50,
    x_label_rotation=0,
    print_values=False,
    interpolate="cubic",
)

html_chart.x_labels = months
html_chart.add("Q1 (Jan-Mar)", list(visitors[:3]) + [None] * 9)
html_chart.add("H1 (Jan-Jun)", list(visitors[:6]) + [None] * 6)
html_chart.add("9 Months (Jan-Sep)", list(visitors[:9]) + [None] * 3)
html_chart.add("Full Year", list(visitors))

html_chart.render_to_file("plot.html")
