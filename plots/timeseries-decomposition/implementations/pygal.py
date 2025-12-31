""" pyplots.ai
timeseries-decomposition: Time Series Decomposition Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 83/100 | Created: 2025-12-31
"""

from io import BytesIO

import cairosvg
import numpy as np
import pandas as pd
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style
from statsmodels.tsa.seasonal import seasonal_decompose


# Data - Monthly CO2 measurements with clear trend and seasonality
np.random.seed(42)
dates = pd.date_range("2020-01-01", periods=72, freq="ME")  # 6 years monthly

# Create realistic CO2-like data with trend, seasonality, and noise
trend = np.linspace(410, 430, 72)  # Rising trend (ppm)
seasonal_pattern = 3 * np.sin(2 * np.pi * np.arange(72) / 12)  # Annual cycle
noise = np.random.normal(0, 0.5, 72)
values = trend + seasonal_pattern + noise

# Create time series and decompose
ts = pd.Series(values, index=dates)
decomposition = seasonal_decompose(ts, model="additive", period=12)

# Extract components
observed = decomposition.observed.values
trend_component = decomposition.trend.values
seasonal_component = decomposition.seasonal.values
residual_component = decomposition.resid.values

# Create x-axis labels (show every 6 months for readability)
x_labels = [d.strftime("%Y-%m") if i % 6 == 0 else "" for i, d in enumerate(dates)]

# Define components with their data, titles, and y-ranges
components = [
    ("Original Series (CO2 ppm)", observed, "#306998", (405, 437)),
    ("Trend Component", trend_component, "#FFD43B", (405, 435)),
    ("Seasonal Component", seasonal_component, "#44AA44", (-5, 5)),
    ("Residual Component", residual_component, "#E74C3C", (-3, 3)),
]

# Target: 4800 x 2700 px total (4 vertically stacked charts)
title_height = 120
chart_width = 4800
chart_height = (2700 - title_height) // 4  # Each chart gets equal height

charts = []
for idx, (label, data, color, y_range) in enumerate(components):
    # Replace NaN with None for pygal
    clean_data = [None if np.isnan(v) else float(v) for v in data]

    # Create custom style with component color
    component_style = Style(
        background="white",
        plot_background="#fafafa",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=(color,),
        font_family="sans-serif",
        title_font_size=32,
        label_font_size=22,
        major_label_font_size=18,
        legend_font_size=22,
        value_font_size=16,
        stroke_width=3,
    )

    chart = pygal.Line(
        width=chart_width,
        height=chart_height,
        style=component_style,
        title=label,
        x_title="Date" if idx == 3 else "",  # Only bottom chart has x-axis title
        y_title="Value",
        show_legend=False,
        show_y_guides=True,
        show_x_guides=True,
        show_dots=False,
        stroke_style={"width": 3},
        range=y_range,
        truncate_label=-1,
        x_label_rotation=45 if idx == 3 else 0,
    )

    # Only show x-labels on the bottom chart
    if idx == 3:
        chart.x_labels = x_labels
    else:
        chart.x_labels = [""] * len(dates)

    chart.add(label, clean_data)
    charts.append(chart)

# Render each chart to PNG and combine them vertically
images = []
for chart in charts:
    svg_bytes = chart.render()
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes, output_width=chart_width, output_height=chart_height)
    img = Image.open(BytesIO(png_bytes))
    images.append(img)

# Create combined image (4800 x 2700)
total_width = 4800
total_height = 2700

combined = Image.new("RGB", (total_width, total_height), "white")

# Add main title
draw = ImageDraw.Draw(combined)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
except OSError:
    title_font = ImageFont.load_default()

title_text = "timeseries-decomposition · pygal · pyplots.ai"
bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = bbox[2] - bbox[0]
title_x = (total_width - title_width) // 2
draw.text((title_x, 35), title_text, fill="#333333", font=title_font)

# Paste charts vertically
for idx, img in enumerate(images):
    y_position = title_height + idx * chart_height
    combined.paste(img, (0, y_position))

# Save final image
combined.save("plot.png", dpi=(300, 300))

# Also save as HTML (interactive SVG)
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>timeseries-decomposition · pygal · pyplots.ai</title>
    <style>
        body { font-family: sans-serif; background: white; margin: 20px; }
        h1 { text-align: center; color: #333; font-size: 28px; margin-bottom: 20px; }
        .charts { display: flex; flex-direction: column; max-width: 1200px; margin: 0 auto; }
        .chart { width: 100%; margin-bottom: 10px; }
        .chart svg { width: 100%; height: auto; }
    </style>
</head>
<body>
    <h1>timeseries-decomposition · pygal · pyplots.ai</h1>
    <div class="charts">
"""

for chart in charts:
    svg_data = chart.render(is_unicode=True)
    svg_data = svg_data.replace('<?xml version="1.0" encoding="utf-8"?>', "")
    html_content += f'        <div class="chart">{svg_data}</div>\n'

html_content += """    </div>
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
