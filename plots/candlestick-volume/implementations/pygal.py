"""pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: pygal 3.1.0 | Python 3.13.11
Quality: 48/100 | Created: 2025-12-31
"""

import os

import numpy as np
import pygal
from PIL import Image
from pygal.style import Style


# Data - Generate 60 trading days of OHLC data with volume
np.random.seed(42)
n_days = 60

# Generate realistic stock price data
base_price = 150.0
returns = np.random.normal(0.001, 0.02, n_days)
close_prices = base_price * np.cumprod(1 + returns)

# Generate OHLC based on close prices
open_prices = np.zeros(n_days)
high_prices = np.zeros(n_days)
low_prices = np.zeros(n_days)
open_prices[0] = base_price
for i in range(n_days):
    if i > 0:
        open_prices[i] = close_prices[i - 1] * (1 + np.random.normal(0, 0.005))
    daily_range = abs(close_prices[i] - open_prices[i]) + np.random.uniform(0.5, 3.0)
    high_prices[i] = max(open_prices[i], close_prices[i]) + np.random.uniform(0.2, daily_range * 0.5)
    low_prices[i] = min(open_prices[i], close_prices[i]) - np.random.uniform(0.2, daily_range * 0.5)

# Generate volume data (higher on volatile days)
base_volume = 5_000_000
volatility = np.abs(close_prices - open_prices) / open_prices
volumes = base_volume * (1 + volatility * 10) * np.random.uniform(0.7, 1.3, n_days)

# Determine bullish (close > open) or bearish (close < open) days
bullish = close_prices > open_prices

# Colors for bullish (green) and bearish (red)
bullish_color = "#2E7D32"  # Dark green
bearish_color = "#C62828"  # Dark red
wick_color = "#555555"  # Gray for wicks

# Custom style for the OHLC price chart (upper pane ~75%)
price_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(wick_color, bullish_color, bearish_color),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=2,
    opacity=1.0,
    opacity_hover=1.0,
)

# Use XY scatter for OHLC representation
# For candlestick approximation we show:
# - High-low wicks as a thin line connecting high and low
# - Open-close body as dots: green for bullish, red for bearish
chart = pygal.XY(
    width=4800,
    height=2025,  # 75% of 2700 for price pane
    style=price_style,
    title="candlestick-volume · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Price ($)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    show_dots=True,
    dots_size=10,
    stroke=True,
    stroke_style={"width": 2},
    show_y_guides=True,
    show_x_guides=False,
    margin=60,
    spacing=20,
    x_label_rotation=45,
    range=(int(min(low_prices) - 5), int(max(high_prices) + 5)),
)

# Create data series for wicks (vertical lines from low to high)
# We'll create individual wick lines for each day
wick_data = []
for i in range(n_days):
    day = i + 1
    # Add low point and high point to draw wick
    wick_data.append((day, round(low_prices[i], 2)))
    wick_data.append((day, round(high_prices[i], 2)))
    # Add None to break line between days
    wick_data.append(None)

# Create separate data for bullish and bearish close prices (body markers)
bullish_close_data = []
bearish_close_data = []
bullish_open_data = []
bearish_open_data = []

for i in range(n_days):
    day = i + 1
    if bullish[i]:
        bullish_close_data.append((day, round(close_prices[i], 2)))
        bullish_open_data.append((day, round(open_prices[i], 2)))
        bearish_close_data.append(None)
        bearish_open_data.append(None)
    else:
        bearish_close_data.append((day, round(close_prices[i], 2)))
        bearish_open_data.append((day, round(open_prices[i], 2)))
        bullish_close_data.append(None)
        bullish_open_data.append(None)

# Add wicks first (background)
chart.add("High-Low Range", wick_data, stroke_style={"width": 3}, dots_size=0, show_dots=False)

# Add bullish markers (green) - larger dots for close, smaller for open
chart.add("Bullish Close", bullish_close_data, stroke=False, dots_size=16, show_dots=True)
chart.add("Bearish Close", bearish_close_data, stroke=False, dots_size=16, show_dots=True)

# X-axis labels
chart.x_labels = [str(i + 1) if i % 10 == 0 else "" for i in range(n_days)]

# Volume chart (lower pane ~25%)
volume_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(bullish_color, bearish_color),
    title_font_size=40,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    stroke_width=1,
    opacity=0.85,
    opacity_hover=1.0,
)

volume_chart = pygal.Bar(
    width=4800,
    height=675,  # 25% of 2700 for volume pane
    style=volume_style,
    x_title="Trading Day",
    y_title="Volume (M)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=20,
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=45,
    truncate_label=10,
    margin=50,
    spacing=20,
    print_values=False,
)

# Separate volume into bullish and bearish for color coding
bullish_volumes = []
bearish_volumes = []

for i in range(n_days):
    vol_millions = round(volumes[i] / 1_000_000, 2)
    if bullish[i]:
        bullish_volumes.append(vol_millions)
        bearish_volumes.append(None)
    else:
        bullish_volumes.append(None)
        bearish_volumes.append(vol_millions)

volume_chart.add("Bullish Volume", bullish_volumes)
volume_chart.add("Bearish Volume", bearish_volumes)

# X-axis labels for volume - show every 10th day
volume_chart.x_labels = [f"Day {i + 1}" if i % 10 == 0 else "" for i in range(n_days)]

# Render both charts to PNG
chart.render_to_png("plot_price.png")
volume_chart.render_to_png("plot_volume.png")

# Create combined HTML with both charts stacked
price_svg = chart.render(is_unicode=True)
volume_svg = volume_chart.render(is_unicode=True)

combined_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>candlestick-volume · pygal · pyplots.ai</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
        }}
        .chart-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0;
        }}
        .price-chart {{
            width: 100%;
        }}
        .volume-chart {{
            width: 100%;
        }}
        svg {{
            width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="price-chart">
            {price_svg}
        </div>
        <div class="volume-chart">
            {volume_svg}
        </div>
    </div>
</body>
</html>
"""

with open("plot.html", "w") as f:
    f.write(combined_html)

# Create combined PNG by stacking the two chart images
price_img = Image.open("plot_price.png")
volume_img = Image.open("plot_volume.png")

# Create combined image
combined_width = max(price_img.width, volume_img.width)
combined_height = price_img.height + volume_img.height

combined_img = Image.new("RGB", (combined_width, combined_height), "white")
combined_img.paste(price_img, (0, 0))
combined_img.paste(volume_img, (0, price_img.height))

combined_img.save("plot.png")

# Clean up intermediate files
os.remove("plot_price.png")
os.remove("plot_volume.png")
