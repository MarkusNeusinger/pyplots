"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

from io import BytesIO

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - Product sales across regions and quarters
np.random.seed(42)

regions = ["North", "South", "East"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate sales data for each region and quarter
data = {}
for region in regions:
    for quarter in quarters:
        base_sales = {"North": 150, "South": 120, "East": 180}[region]
        quarter_factor = {"Q1": 0.8, "Q2": 1.0, "Q3": 1.1, "Q4": 1.3}[quarter]
        months = (
            ["Jan", "Feb", "Mar"]
            if quarter == "Q1"
            else ["Apr", "May", "Jun"]
            if quarter == "Q2"
            else ["Jul", "Aug", "Sep"]
            if quarter == "Q3"
            else ["Oct", "Nov", "Dec"]
        )
        sales = [base_sales * quarter_factor * (1 + np.random.uniform(-0.15, 0.15)) for _ in months]
        data[(region, quarter)] = {"months": months, "sales": sales}

# Custom style for pygal
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#FF5722"),
    font_family="sans-serif",
    title_font_size=36,
    label_font_size=24,
    major_label_font_size=22,
    legend_font_size=20,
    value_font_size=18,
    stroke_width=3,
)

# Create individual charts for each facet
# Grid: 3 rows (regions) x 4 columns (quarters)
# Target: 4800 x 2700 px total
chart_width = 1200
chart_height = 800
charts_per_row = 4
charts_per_col = 3
title_height = 100

# Store rendered chart images
chart_images = []

for region in regions:
    row_images = []
    for quarter in quarters:
        facet_data = data[(region, quarter)]

        # Create bar chart for this facet
        chart = pygal.Bar(
            width=chart_width,
            height=chart_height,
            style=custom_style,
            title=f"{region} - {quarter}",
            x_title="Month",
            y_title="Sales ($K)",
            show_legend=False,
            show_y_guides=True,
            show_x_guides=False,
            y_labels_major_every=2,
            truncate_label=-1,
            margin=40,
            margin_top=70,
            range=(0, 300),  # Fixed y-axis range for comparison
        )

        chart.x_labels = facet_data["months"]
        chart.add("Sales", facet_data["sales"])

        # Render to PNG bytes
        png_bytes = chart.render_to_png()
        img = Image.open(BytesIO(png_bytes))
        row_images.append(img)

    chart_images.append(row_images)

# Combine all charts into a grid
total_width = chart_width * charts_per_row  # 4800
total_height = chart_height * charts_per_col + title_height  # 2500

# Create combined image (4800 x 2700 target)
combined = Image.new("RGB", (4800, 2700), "white")

# Add main title using PIL text drawing
draw = ImageDraw.Draw(combined)
title_text = "facet-grid . pygal . pyplots.ai"
# Try to use a font, fall back to default if not available
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
except (OSError, IOError):
    font = ImageFont.load_default()

# Get text bounding box for centering
bbox = draw.textbbox((0, 0), title_text, font=font)
text_width = bbox[2] - bbox[0]
text_x = (4800 - text_width) // 2
draw.text((text_x, 30), title_text, fill="#333333", font=font)

# Paste each chart into the grid
for row_idx, row_images in enumerate(chart_images):
    for col_idx, img in enumerate(row_images):
        x_offset = col_idx * chart_width
        y_offset = title_height + row_idx * chart_height
        combined.paste(img, (x_offset, y_offset))

# Save as PNG
combined.save("plot.png", dpi=(300, 300))

# Also save as HTML (interactive SVG grid)
# Create an HTML file with embedded SVGs
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>facet-grid - pygal - pyplots.ai</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background: white; }
        h1 { text-align: center; color: #333; font-size: 32px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; max-width: 100%; }
        .facet { border: 1px solid #eee; border-radius: 4px; }
        .facet svg { width: 100%; height: auto; }
    </style>
</head>
<body>
    <h1>facet-grid &middot; pygal &middot; pyplots.ai</h1>
    <div class="grid">
"""

# Add each facet as embedded SVG
for region in regions:
    for quarter in quarters:
        facet_data = data[(region, quarter)]

        chart = pygal.Bar(
            width=600,
            height=400,
            style=custom_style,
            title=f"{region} - {quarter}",
            x_title="Month",
            y_title="Sales ($K)",
            show_legend=False,
            show_y_guides=True,
            show_x_guides=False,
            range=(0, 300),
        )

        chart.x_labels = facet_data["months"]
        chart.add("Sales", facet_data["sales"])

        svg_content = chart.render(is_unicode=True)
        html_content += f'<div class="facet">{svg_content}</div>\n'

html_content += """
    </div>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
