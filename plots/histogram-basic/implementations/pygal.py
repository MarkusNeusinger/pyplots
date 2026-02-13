"""pyplots.ai
histogram-basic: Basic Histogram
Library: pygal 3.1.0 | Python 3.14.0
Quality: 81/100 | Created: 2025-12-23
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - Exam scores with realistic right skew using beta distribution
np.random.seed(42)
n = 500
# Beta distribution (a=5, b=2) naturally skews right and tapers at both ends
raw = np.random.beta(a=5, b=2, size=n)
values = raw * 60 + 35  # Scale to ~35-95 range (realistic exam scores)

# Compute histogram bins
n_bins = 25
counts, bin_edges = np.histogram(values, bins=n_bins)
hist_data = [(int(count), float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(counts)]

# Key statistics for storytelling
mean_val = float(np.mean(values))
median_val = float(np.median(values))
q1, q3 = float(np.percentile(values, 25)), float(np.percentile(values, 75))
peak_bin = int(np.argmax(counts))
peak_lo, peak_hi = float(bin_edges[peak_bin]), float(bin_edges[peak_bin + 1])

# Shared font family
font = "DejaVu Sans, Helvetica, Arial, sans-serif"

# Custom style — refined typography, subtle grid, polished chrome
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2d2d2d",
    foreground_strong="#2d2d2d",
    foreground_subtle="#e8e8e8",
    colors=("#306998", "#c0392b", "#27ae60"),
    font_family=font,
    title_font_family=font,
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    legend_font_family=font,
    value_font_size=30,
    opacity=0.85,
    opacity_hover=0.95,
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="4,4",
    major_guide_stroke_color="#d0d0d0",
    major_guide_stroke_dasharray="6,3",
    stroke_opacity=1.0,
    tooltip_font_size=28,
    tooltip_font_family=font,
    tooltip_border_radius=10,
)

# Create histogram chart
chart = pygal.Histogram(
    width=4800,
    height=2700,
    style=custom_style,
    title="histogram-basic · pygal · pyplots.ai",
    x_title="Exam Score (points)",
    y_title="Number of Students",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    show_y_guides=True,
    show_x_guides=False,
    value_formatter=lambda x: f"{x:,.0f}",
    tooltip_fancy_mode=True,
    min_scale=4,
    max_scale=8,
    margin_bottom=120,
    margin_left=80,
    margin_right=60,
    margin_top=60,
    spacing=12,
    print_values=False,
)

# Main histogram series
chart.add("Score Distribution (n=500)", hist_data)

# Mean marker — tall narrow bar as vertical reference line
marker_h = int(max(counts))
chart.add(f"Mean: {mean_val:.1f} pts", [(marker_h, mean_val - 0.5, mean_val + 0.5)], stroke_style={"width": 3})

# IQR band — prominent shaded region showing central 50%
iqr_height = int(max(counts) * 0.30)
chart.add(f"IQR: {q1:.0f}\u2013{q3:.0f} pts (middle 50%)", [(iqr_height, q1, q3)], stroke_style={"width": 2})

# Render chart to PNG in memory for annotation overlay
chart_png = chart.render_to_png()
img = Image.open(io.BytesIO(chart_png))
draw = ImageDraw.Draw(img)

# Load fonts for annotations
try:
    ann_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    ann_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
except OSError:
    ann_font = ImageFont.load_default()
    ann_bold = ann_font

# Annotation: summary statistics box in upper-left area (above low-count bins)
box_x, box_y = 450, 180
box_w, box_h = 1020, 380
draw.rounded_rectangle(
    [(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=18, fill="#ffffffd9", outline="#b0b0b0", width=2
)
draw.text((box_x + 30, box_y + 22), "Distribution Summary", fill="#2d2d2d", font=ann_bold)
draw.line([(box_x + 30, box_y + 72), (box_x + box_w - 30, box_y + 72)], fill="#d0d0d0", width=2)
stats_lines = [
    f"Mean: {mean_val:.1f}  |  Median: {median_val:.1f}",
    f"Spread (IQR): {q1:.0f} \u2013 {q3:.0f} pts",
    f"Peak bin: {peak_lo:.0f}\u2013{peak_hi:.0f} pts ({int(counts[peak_bin])} students)",
    "Skew: left-skewed (mean < median)",
]
ly = box_y + 88
for line in stats_lines:
    draw.text((box_x + 30, ly), line, fill="#444444", font=ann_font)
    ly += 62

# Annotation: callout above the peak bin
# Map peak bin center from data coordinates to approximate pixel position
data_min, data_max = float(bin_edges[0]), float(bin_edges[-1])
peak_mid = (peak_lo + peak_hi) / 2
plot_x0, plot_x1 = 350, 4650  # approximate plot area x-bounds in 4800px image
peak_px = plot_x0 + (peak_mid - data_min) / (data_max - data_min) * (plot_x1 - plot_x0)
label_text = f"\u25bc Peak: {peak_lo:.0f}\u2013{peak_hi:.0f} pts"
bbox = draw.textbbox((0, 0), label_text, font=ann_bold)
label_w = bbox[2] - bbox[0]
draw.text((int(peak_px - label_w / 2), 120), label_text, fill="#306998", font=ann_bold)

# Save annotated image
img.save("plot.png", "PNG")

# Save interactive HTML version (without PIL annotations)
chart.render_to_file("plot.html")
