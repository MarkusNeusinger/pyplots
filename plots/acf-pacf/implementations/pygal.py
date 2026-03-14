""" pyplots.ai
acf-pacf: Autocorrelation and Partial Autocorrelation (ACF/PACF) Plot
Library: pygal 3.1.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-14
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style
from statsmodels.tsa.stattools import acf, pacf


# Data - Synthetic monthly airline-style passenger data with trend and seasonality
np.random.seed(42)
n_obs = 200
t = np.arange(n_obs)
trend = 0.05 * t
seasonal = 10 * np.sin(2 * np.pi * t / 12)
noise = np.random.normal(0, 2, n_obs)
passengers = 100 + trend + seasonal + noise

# Compute ACF and PACF
n_lags = 36
acf_values = acf(passengers, nlags=n_lags, fft=True)
pacf_values = pacf(passengers, nlags=n_lags, method="ywm")
conf_bound = 1.96 / np.sqrt(n_obs)

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2C3E50",
    foreground_strong="#2C3E50",
    foreground_subtle="#E0E0E0",
    colors=("#306998",),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=20,
    font_family="sans-serif",
    title_font_family="sans-serif",
    label_font_family="sans-serif",
    value_font_family="sans-serif",
)

# Highlight color for significant lags
highlight_color = "#306998"
muted_color = "#A8C4D8"


# ACF chart
acf_chart = pygal.Bar(
    width=4800,
    height=1200,
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
    x_title="",
    y_title="ACF",
    title="",
    margin=20,
    margin_bottom=10,
    margin_top=40,
    margin_left=80,
    margin_right=40,
    spacing=2,
    range=(-0.5, 1.1),
    truncate_label=-1,
    print_values=False,
)

acf_lags = list(range(n_lags + 1))
acf_chart.x_labels = [str(i) if i % 5 == 0 else "" for i in acf_lags]

acf_bar_data = []
for v in acf_values:
    color = highlight_color if abs(v) > conf_bound else muted_color
    acf_bar_data.append({"value": round(v, 4), "color": color})

acf_chart.add("ACF", acf_bar_data)

# PACF chart
pacf_chart = pygal.Bar(
    width=4800,
    height=1200,
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
    x_title="Lag",
    y_title="PACF",
    title="",
    margin=20,
    margin_bottom=60,
    margin_top=10,
    margin_left=80,
    margin_right=40,
    spacing=2,
    range=(-0.5, 1.1),
    truncate_label=-1,
    print_values=False,
)

pacf_lags = list(range(1, n_lags + 1))
pacf_chart.x_labels = [str(i) if i % 5 == 0 else "" for i in pacf_lags]

pacf_bar_data = []
for v in pacf_values[1:]:
    color = highlight_color if abs(v) > conf_bound else muted_color
    pacf_bar_data.append({"value": round(v, 4), "color": color})

pacf_chart.add("PACF", pacf_bar_data)

# Render both charts to PNG and combine
acf_png = acf_chart.render_to_png()
pacf_png = pacf_chart.render_to_png()

acf_img = Image.open(io.BytesIO(acf_png))
pacf_img = Image.open(io.BytesIO(pacf_png))

# Combine into single 4800x2700 image
total_width = 4800
total_height = 2700
title_height = 200

combined = Image.new("RGB", (total_width, total_height), "white")

# Resize charts to fit
chart_height = (total_height - title_height) // 2
acf_resized = acf_img.resize((total_width, chart_height), Image.LANCZOS)
pacf_resized = pacf_img.resize((total_width, chart_height), Image.LANCZOS)

combined.paste(acf_resized, (0, title_height))
combined.paste(pacf_resized, (0, title_height + chart_height))

# Add title and confidence bound annotations
draw = ImageDraw.Draw(combined)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

title_text = "acf-pacf \u00b7 pygal \u00b7 pyplots.ai"
bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_w = bbox[2] - bbox[0]
draw.text(((total_width - title_w) // 2, 40), title_text, fill="#2C3E50", font=title_font)

subtitle_text = f"Monthly Passenger Data (n={n_obs}) \u00b7 95% confidence bounds at \u00b1{conf_bound:.3f}"
bbox2 = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
sub_w = bbox2[2] - bbox2[0]
draw.text(((total_width - sub_w) // 2, 130), subtitle_text, fill="#666666", font=subtitle_font)

# Draw confidence bound lines on both charts
for chart_y_offset in [title_height, title_height + chart_height]:
    # Calculate pixel positions for confidence bounds within chart area
    # The chart plot area is roughly 80% of chart height, offset from top
    plot_top = chart_y_offset + int(chart_height * 0.08)
    plot_bottom = chart_y_offset + int(chart_height * 0.88)
    plot_left = int(total_width * 0.04)
    plot_right = int(total_width * 0.98)
    plot_range_height = plot_bottom - plot_top
    value_range = 1.1 - (-0.5)

    # Convert correlation value to y pixel
    upper_y = int(plot_top + (1.1 - conf_bound) / value_range * plot_range_height)
    lower_y = int(plot_top + (1.1 + conf_bound) / value_range * plot_range_height)
    zero_y = int(plot_top + 1.1 / value_range * plot_range_height)

    # Dashed confidence lines
    dash_length = 20
    gap_length = 12
    for line_y in [upper_y, lower_y]:
        x = plot_left
        while x < plot_right:
            draw.line([(x, line_y), (min(x + dash_length, plot_right), line_y)], fill="#E74C3C", width=3)
            x += dash_length + gap_length

# Save
combined.save("plot.png", dpi=(300, 300))

# HTML version with interactive SVGs
acf_svg = acf_chart.render(is_unicode=True).replace('<?xml version="1.0" encoding="utf-8"?>', "")
pacf_svg = pacf_chart.render(is_unicode=True).replace('<?xml version="1.0" encoding="utf-8"?>', "")

html_content = (
    "<!DOCTYPE html>\n<html>\n<head>\n"
    "    <title>acf-pacf \u00b7 pygal \u00b7 pyplots.ai</title>\n"
    "    <style>\n"
    "        body { font-family: sans-serif; background: white; margin: 0; padding: 20px; }\n"
    "        h1 { text-align: center; color: #2C3E50; font-size: 28px; margin-bottom: 5px; }\n"
    "        p.subtitle { text-align: center; color: #666; font-size: 16px; margin-top: 0; }\n"
    "        .container { max-width: 1200px; margin: 0 auto; }\n"
    "        .chart { width: 100%%; margin: 10px 0; }\n"
    "    </style>\n</head>\n<body>\n"
    "    <div class='container'>\n"
    "        <h1>acf-pacf \u00b7 pygal \u00b7 pyplots.ai</h1>\n"
    "        <p class='subtitle'>Monthly Passenger Data \u00b7 95% confidence bounds shown</p>\n"
    "        <div class='chart'>" + acf_svg + "</div>\n"
    "        <div class='chart'>" + pacf_svg + "</div>\n"
    "    </div>\n</body>\n</html>"
)

with open("plot.html", "w") as f:
    f.write(html_content)
