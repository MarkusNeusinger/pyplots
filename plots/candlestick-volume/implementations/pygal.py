"""pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: pygal 3.1.0 | Python 3.13.11
Quality: 52/100 | Created: 2025-12-31
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

# Custom style for the OHLC price chart (upper pane ~75%)
price_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(bullish_color, bearish_color, "#888888", "#888888"),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=3,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create a chart showing OHLC as range bars (using min-max for each day)
# Pygal StackedBar can show ranges by stacking from baseline
# We use a custom approach: Line chart with high/low as filled range
chart = pygal.Line(
    width=4800,
    height=2025,  # 75% of 2700 for price pane
    style=price_style,
    title="candlestick-volume · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Price ($)",
    show_dots=True,
    dots_size=8,
    stroke_style={"width": 4},
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    fill=False,
    range=(int(min(low_prices) - 5), int(max(high_prices) + 5)),
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=45,
    truncate_label=10,
    margin=60,
    spacing=25,
    interpolate=None,  # No interpolation - connect with straight lines
)

# Create separate series for bullish and bearish days to show color differentiation
# For candlestick approximation, we show:
# - High line (dashed gray) - shows the upper wick
# - Low line (dashed gray) - shows the lower wick
# - Close (bullish days) - solid green dots
# - Close (bearish days) - solid red dots
# - Open line for reference

bullish_close = []
bearish_close = []

for i in range(n_days):
    if bullish[i]:
        bullish_close.append({"value": round(close_prices[i], 2), "color": bullish_color})
        bearish_close.append(None)
    else:
        bullish_close.append(None)
        bearish_close.append({"value": round(close_prices[i], 2), "color": bearish_color})

# Add series - using dots to show close prices with color coding
chart.add("Bullish Close", bullish_close, stroke_style={"width": 0}, dots_size=12, show_dots=True)
chart.add("Bearish Close", bearish_close, stroke_style={"width": 0}, dots_size=12, show_dots=True)
# Add high/low as subtle reference lines
chart.add(
    "High",
    [round(p, 2) for p in high_prices],
    stroke_style={"width": 2, "dasharray": "5,5"},
    dots_size=3,
    show_dots=True,
)
chart.add(
    "Low", [round(p, 2) for p in low_prices], stroke_style={"width": 2, "dasharray": "5,5"}, dots_size=3, show_dots=True
)

# X-axis labels - show every 10th day for readability
chart.x_labels = [f"Day {i + 1}" if i % 10 == 0 else "" for i in range(n_days)]

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
    opacity=0.8,
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
