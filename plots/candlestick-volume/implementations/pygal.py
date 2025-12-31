""" pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: pygal 3.1.0 | Python 3.13.11
Quality: 52/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
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

# Custom style for the chart
chart_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#2E8B57", "#DC143C", "#9E9E9E"),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=3,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create chart with OHLC lines and volume on secondary axis
# Pygal doesn't have native candlestick, so we use line chart with OHLC series
chart = pygal.Line(
    width=4800,
    height=2700,
    style=chart_style,
    title="Stock OHLC with Volume · candlestick-volume · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Price ($)",
    secondary_range=(0, 12),  # Volume in millions (fixed range for cleaner labels)
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 4},
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    fill=False,
    range=(115, 175),  # Fixed price range for cleaner y-axis
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=45,
    truncate_label=10,
    margin=60,
    spacing=25,
)

# Add price series - Close and Open as main series, High/Low as range indicators
chart.add("Close Price", [round(p, 2) for p in close_prices], stroke_style={"width": 5})
chart.add("Open Price", [round(p, 2) for p in open_prices], stroke_style={"width": 3, "dasharray": "6,4"})
chart.add("High", [round(p, 2) for p in high_prices], stroke_style={"width": 2, "dasharray": "10,5"})
chart.add("Low", [round(p, 2) for p in low_prices], stroke_style={"width": 2, "dasharray": "10,5"})

# Add volume on secondary y-axis as subtle filled area
chart.add(
    "Volume (M)", [round(v / 1_000_000, 1) for v in volumes], secondary=True, stroke_style={"width": 1}, fill=True
)

# X-axis labels - show every 5th day
chart.x_labels = [f"Day {i + 1}" if i % 5 == 0 else "" for i in range(n_days)]

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
