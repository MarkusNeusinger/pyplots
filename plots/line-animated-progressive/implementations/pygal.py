""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-07
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

# Custom style for consistent appearance across all panels
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    font_family="sans-serif",
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=32,
    stroke_width=8,
    opacity=0.9,
)

# Fixed y-axis range for all panels (ensures visual consistency)
y_min = int(min(visitors) * 0.9)
y_max = int(max(visitors) * 1.1)

# Panel dimensions
panel_width = 2300
panel_height = 1200

# Chart config shared across all panels
chart_config = {
    "width": panel_width,
    "height": panel_height,
    "style": custom_style,
    "show_x_guides": False,
    "show_y_guides": True,
    "show_dots": True,
    "dots_size": 14,
    "stroke_style": {"width": 8, "linecap": "round", "linejoin": "round"},
    "fill": False,
    "show_legend": False,
    "margin": 60,
    "spacing": 40,
    "x_label_rotation": 0,
    "print_values": False,
    "interpolate": "cubic",
    "range": (y_min, y_max),
}

# Stage 1: Q1 Data (January - March)
chart1 = pygal.Line(title="Stage 1: Q1 Data", x_title="January - March", y_title="Visitors", **chart_config)
chart1.x_labels = months
chart1.add("Traffic", list(visitors[:3]) + [None] * 9)
img1 = Image.open(io.BytesIO(chart1.render_to_png()))

# Stage 2: H1 Data (January - June)
chart2 = pygal.Line(title="Stage 2: H1 Data", x_title="January - June", y_title="Visitors", **chart_config)
chart2.x_labels = months
chart2.add("Traffic", list(visitors[:6]) + [None] * 6)
img2 = Image.open(io.BytesIO(chart2.render_to_png()))

# Stage 3: 9 Months (January - September)
chart3 = pygal.Line(title="Stage 3: 9 Months", x_title="January - September", y_title="Visitors", **chart_config)
chart3.x_labels = months
chart3.add("Traffic", list(visitors[:9]) + [None] * 3)
img3 = Image.open(io.BytesIO(chart3.render_to_png()))

# Stage 4: Full Year (January - December)
chart4 = pygal.Line(title="Stage 4: Full Year", x_title="January - December", y_title="Visitors", **chart_config)
chart4.x_labels = months
chart4.add("Traffic", list(visitors))
img4 = Image.open(io.BytesIO(chart4.render_to_png()))

# Create small multiples layout (2x2 grid)
margin = 100
title_height = 150

# Final canvas: 4800x2700
final_width = 4800
final_height = 2700
final_image = Image.new("RGB", (final_width, final_height), "white")

# Calculate panel positions to center the grid
grid_width = 2 * panel_width + margin
grid_height = 2 * panel_height + margin
x_offset = (final_width - grid_width) // 2
y_offset = title_height + (final_height - title_height - grid_height) // 2

# Paste panels in 2x2 grid
# Top-left: Stage 1
final_image.paste(img1, (x_offset, y_offset))
# Top-right: Stage 2
final_image.paste(img2, (x_offset + panel_width + margin, y_offset))
# Bottom-left: Stage 3
final_image.paste(img3, (x_offset, y_offset + panel_height + margin))
# Bottom-right: Stage 4
final_image.paste(img4, (x_offset + panel_width + margin, y_offset + panel_height + margin))

# Add title at top center using PIL
draw = ImageDraw.Draw(final_image)
title_text = "line-animated-progressive \u00b7 pygal \u00b7 pyplots.ai"
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
    colors=("#306998", "#FFD43B", "#5A9BD5", "#70AD47"),
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
    title="line-animated-progressive \u00b7 pygal \u00b7 pyplots.ai",
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
