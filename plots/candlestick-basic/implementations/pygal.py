""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Stock OHLC data for 30 trading days
np.random.seed(42)
n_days = 30

# Generate realistic OHLC data with trend and volatility
base_price = 150.0
returns = np.random.randn(n_days) * 2.5  # Daily returns in %
price_series = base_price * np.cumprod(1 + returns / 100)

ohlc_data = []
for i, close in enumerate(price_series):
    # Generate realistic intraday range
    volatility = np.abs(np.random.randn()) * 2 + 0.5
    intraday_range = close * volatility / 100

    if i == 0:
        open_price = base_price
    else:
        open_price = ohlc_data[-1]["close"]

    high = max(open_price, close) + np.random.rand() * intraday_range
    low = min(open_price, close) - np.random.rand() * intraday_range

    ohlc_data.append({"day": i + 1, "open": open_price, "high": high, "low": low, "close": close})

# Calculate data range for chart
all_highs = [d["high"] for d in ohlc_data]
all_lows = [d["low"] for d in ohlc_data]
y_min = min(all_lows) - 2
y_max = max(all_highs) + 2

# Colors
bullish_color = "#22A06B"
bearish_color = "#EF4444"

# Build color list - bodies first, then wicks (same order as series)
colors_list = []
for candle in ohlc_data:
    is_bullish = candle["close"] >= candle["open"]
    colors_list.append(bullish_color if is_bullish else bearish_color)
for candle in ohlc_data:
    is_bullish = candle["close"] >= candle["open"]
    colors_list.append(bullish_color if is_bullish else bearish_color)

# Custom style for 4800x2700 output with larger fonts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(colors_list),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=44,
    value_font_size=36,
)

# Create XY chart for candlesticks
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="candlestick-basic · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Price ($)",
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    range=(y_min, y_max),
    xrange=(0, n_days + 1),
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    margin=60,
    spacing=40,
)

# Stroke widths - increased for better visibility on large canvas
wick_width = 16
body_width = 70

# Track legend state
bullish_legend_done = False
bearish_legend_done = False

# Add each candlestick body as a separate series
for candle in ohlc_data:
    day = candle["day"]
    is_bullish = candle["close"] >= candle["open"]

    # Determine legend label
    if is_bullish and not bullish_legend_done:
        label = "Bullish (Up)"
        bullish_legend_done = True
    elif not is_bullish and not bearish_legend_done:
        label = "Bearish (Down)"
        bearish_legend_done = True
    else:
        label = None

    # Body (open to close)
    chart.add(
        label,
        [(day, candle["open"]), (day, candle["close"])],
        stroke=True,
        show_dots=False,
        stroke_style={"width": body_width, "linecap": "butt"},
    )

# Add each wick as a separate series (no legends)
for candle in ohlc_data:
    day = candle["day"]
    chart.add(
        None,
        [(day, candle["low"]), (day, candle["high"])],
        stroke=True,
        show_dots=False,
        stroke_style={"width": wick_width, "linecap": "butt"},
    )

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
