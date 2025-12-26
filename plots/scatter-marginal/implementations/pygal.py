""" pyplots.ai
scatter-marginal: Scatter Plot with Marginal Distributions
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-26
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - correlated bivariate data
np.random.seed(42)
n_points = 150
x = np.random.randn(n_points) * 15 + 50
y = x * 0.6 + np.random.randn(n_points) * 12 + 20

# Calculate histogram data for marginals
n_bins = 15
x_hist, x_edges = np.histogram(x, bins=n_bins)
y_hist, y_edges = np.histogram(y, bins=n_bins)

# Dimensions for layout
total_width = 4800
total_height = 2700
margin_plot_size = 500
title_height = 120
gap = 20

# Calculate main scatter dimensions
scatter_width = total_width - margin_plot_size - gap * 3
scatter_height = total_height - margin_plot_size - title_height - gap * 3

# Custom style for main scatter
scatter_style = Style(
    background="#ffffff",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    tooltip_font_size=24,
    opacity=0.65,
    opacity_hover=0.9,
    guide_stroke_color="#e0e0e0",
    major_guide_stroke_color="#cccccc",
)

# Custom style for marginal histograms
marginal_style = Style(
    background="#ffffff",
    plot_background="#f8f8f8",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=32,
    label_font_size=28,
    major_label_font_size=26,
    legend_font_size=26,
    opacity=0.75,
    guide_stroke_color="#e0e0e0",
)

# Create main scatter plot
scatter = pygal.XY(
    width=scatter_width,
    height=scatter_height,
    style=scatter_style,
    x_title="X Value",
    y_title="Y Value",
    show_legend=False,
    stroke=False,
    dots_size=10,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_label=-1,
    explicit_size=True,
    margin_top=30,
    margin_right=30,
    margin_bottom=80,
    margin_left=100,
)

# Add scatter data
scatter_points = [(float(xi), float(yi)) for xi, yi in zip(x, y, strict=True)]
scatter.add("Data", scatter_points)

# Create top marginal histogram (X distribution)
x_margin = pygal.Bar(
    width=scatter_width,
    height=margin_plot_size,
    style=marginal_style,
    show_legend=False,
    show_x_labels=False,
    show_y_labels=True,
    show_y_guides=True,
    show_x_guides=False,
    margin_top=30,
    margin_right=30,
    margin_bottom=30,
    margin_left=100,
    explicit_size=True,
    spacing=4,
)
x_margin.add("X Distribution", [float(h) for h in x_hist])

# Create right marginal histogram (Y distribution) - horizontal bars
y_margin = pygal.HorizontalBar(
    width=margin_plot_size,
    height=scatter_height,
    style=marginal_style,
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    show_y_guides=False,
    show_x_guides=False,
    margin_top=30,
    margin_right=40,
    margin_bottom=80,
    margin_left=10,
    explicit_size=True,
    spacing=4,
)
# Reverse order to match scatter Y axis orientation (pygal HorizontalBar goes top-to-bottom)
y_margin.add("Y Distribution", [float(h) for h in y_hist[::-1]])

# Render each chart to PNG in memory
scatter_png = scatter.render_to_png()
x_margin_png = x_margin.render_to_png()
y_margin_png = y_margin.render_to_png()

# Open images
scatter_img = Image.open(io.BytesIO(scatter_png))
x_margin_img = Image.open(io.BytesIO(x_margin_png))
y_margin_img = Image.open(io.BytesIO(y_margin_png))

# Create final composite image
final_img = Image.new("RGB", (total_width, total_height), "white")

# Calculate positions
scatter_x = gap
scatter_y = title_height + margin_plot_size + gap
x_margin_x = gap
x_margin_y = title_height
y_margin_x = gap + scatter_width + gap
y_margin_y = title_height + margin_plot_size + gap

# Paste images
final_img.paste(x_margin_img, (x_margin_x, x_margin_y))
final_img.paste(y_margin_img, (y_margin_x, y_margin_y))
final_img.paste(scatter_img, (scatter_x, scatter_y))

# Add title
draw = ImageDraw.Draw(final_img)
title_text = "scatter-marginal · pygal · pyplots.ai"
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
except OSError:
    font = ImageFont.load_default()

# Get text bounding box for centering
bbox = draw.textbbox((0, 0), title_text, font=font)
text_width = bbox[2] - bbox[0]
text_x = (total_width - text_width) // 2
text_y = 40
draw.text((text_x, text_y), title_text, fill="#333333", font=font)

# Save final image
final_img.save("plot.png", "PNG")

# Also save the scatter SVG as HTML for interactivity
scatter_svg_full = scatter.render().decode("utf-8")
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(scatter_svg_full)
