""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import math
import xml.etree.ElementTree as ET

import cairosvg


# Data - 30 trading days of stock OHLC data
dates = [
    "Jan 02",
    "Jan 03",
    "Jan 06",
    "Jan 07",
    "Jan 08",
    "Jan 09",
    "Jan 10",
    "Jan 13",
    "Jan 14",
    "Jan 15",
    "Jan 16",
    "Jan 17",
    "Jan 21",
    "Jan 22",
    "Jan 23",
    "Jan 24",
    "Jan 27",
    "Jan 28",
    "Jan 29",
    "Jan 30",
    "Jan 31",
    "Feb 03",
    "Feb 04",
    "Feb 05",
    "Feb 06",
    "Feb 07",
    "Feb 10",
    "Feb 11",
    "Feb 12",
    "Feb 13",
]

# OHLC data: (open, high, low, close)
ohlc_data = [
    (150.00, 152.50, 149.00, 151.80),
    (151.80, 154.20, 151.00, 153.50),
    (153.50, 155.00, 152.80, 153.20),
    (153.20, 153.80, 150.50, 151.00),
    (151.00, 152.00, 148.50, 149.20),
    (149.20, 151.50, 148.80, 151.00),
    (151.00, 154.00, 150.50, 153.80),
    (153.80, 156.50, 153.00, 156.00),
    (156.00, 158.00, 155.20, 157.50),
    (157.50, 159.00, 156.00, 156.80),
    (156.80, 157.50, 154.00, 154.50),
    (154.50, 155.80, 153.00, 155.20),
    (155.20, 158.00, 154.80, 157.80),
    (157.80, 160.50, 157.00, 160.00),
    (160.00, 161.20, 158.50, 159.00),
    (159.00, 159.50, 156.00, 156.50),
    (156.50, 158.00, 155.00, 157.50),
    (157.50, 159.50, 156.80, 159.00),
    (159.00, 162.00, 158.50, 161.50),
    (161.50, 163.00, 160.00, 160.80),
    (160.80, 161.50, 158.00, 158.50),
    (158.50, 160.00, 157.00, 159.50),
    (159.50, 162.50, 159.00, 162.00),
    (162.00, 165.00, 161.50, 164.50),
    (164.50, 166.00, 163.00, 163.50),
    (163.50, 164.00, 160.50, 161.00),
    (161.00, 163.00, 160.00, 162.50),
    (162.50, 165.50, 162.00, 165.00),
    (165.00, 167.00, 164.00, 166.50),
    (166.50, 168.50, 165.50, 168.00),
]

# Chart dimensions
WIDTH = 4800
HEIGHT = 2700
MARGIN_LEFT = 200
MARGIN_RIGHT = 100
MARGIN_TOP = 180
MARGIN_BOTTOM = 280

# Plot area
plot_width = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
plot_height = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Calculate price range
all_prices = [p for ohlc in ohlc_data for p in ohlc]
price_min = min(all_prices) - 2
price_max = max(all_prices) + 2
price_range = price_max - price_min

# Colors
BULLISH_COLOR = "#22A06B"  # Green for up
BEARISH_COLOR = "#E53935"  # Red for down
GRID_COLOR = "#E0E0E0"
TEXT_COLOR = "#333333"


def price_to_y(price):
    """Convert price to y coordinate (inverted because SVG y increases downward)."""
    return MARGIN_TOP + plot_height - ((price - price_min) / price_range * plot_height)


def idx_to_x(idx):
    """Convert index to x coordinate."""
    spacing = plot_width / (len(ohlc_data) + 1)
    return MARGIN_LEFT + spacing * (idx + 1)


# Create SVG
svg = ET.Element(
    "svg", xmlns="http://www.w3.org/2000/svg", width=str(WIDTH), height=str(HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}"
)

# White background
ET.SubElement(svg, "rect", x="0", y="0", width=str(WIDTH), height=str(HEIGHT), fill="white")

# Title
title = ET.SubElement(
    svg,
    "text",
    x=str(WIDTH // 2),
    y="80",
    fill=TEXT_COLOR,
    style="font-family: sans-serif; font-size: 60px; font-weight: bold;",
)
title.set("text-anchor", "middle")
title.text = "Stock Price OHLC · candlestick-basic · pygal · pyplots.ai"

# Y-axis label
y_label = ET.SubElement(
    svg,
    "text",
    x="60",
    y=str(HEIGHT // 2),
    fill=TEXT_COLOR,
    style="font-family: sans-serif; font-size: 40px;",
    transform=f"rotate(-90, 60, {HEIGHT // 2})",
)
y_label.set("text-anchor", "middle")
y_label.text = "Price ($)"

# X-axis label
x_label = ET.SubElement(
    svg,
    "text",
    x=str(WIDTH // 2),
    y=str(HEIGHT - 40),
    fill=TEXT_COLOR,
    style="font-family: sans-serif; font-size: 40px;",
)
x_label.set("text-anchor", "middle")
x_label.text = "Date"

# Y-axis grid and labels
nice_interval = 5
y_start = math.ceil(price_min / nice_interval) * nice_interval
for price in range(int(y_start), int(price_max) + 1, nice_interval):
    y = price_to_y(price)
    if MARGIN_TOP <= y <= MARGIN_TOP + plot_height:
        # Grid line
        ET.SubElement(
            svg,
            "line",
            x1=str(MARGIN_LEFT),
            y1=str(y),
            x2=str(WIDTH - MARGIN_RIGHT),
            y2=str(y),
            stroke=GRID_COLOR,
            style="stroke-width: 2;",
        )
        # Label
        y_tick = ET.SubElement(
            svg,
            "text",
            x=str(MARGIN_LEFT - 20),
            y=str(y + 10),
            fill=TEXT_COLOR,
            style="font-family: sans-serif; font-size: 32px;",
        )
        y_tick.set("text-anchor", "end")
        y_tick.text = f"${price}"

# Plot area border
ET.SubElement(
    svg,
    "rect",
    x=str(MARGIN_LEFT),
    y=str(MARGIN_TOP),
    width=str(plot_width),
    height=str(plot_height),
    fill="none",
    stroke="#CCCCCC",
    style="stroke-width: 2;",
)

# Draw candlesticks
candle_width = plot_width / (len(ohlc_data) + 1) * 0.6

for i, (open_price, high, low, close) in enumerate(ohlc_data):
    x = idx_to_x(i)
    is_bullish = close >= open_price

    # Color based on direction
    fill_color = BULLISH_COLOR if is_bullish else BEARISH_COLOR

    # Wick (high-low line)
    y_high = price_to_y(high)
    y_low = price_to_y(low)
    ET.SubElement(
        svg, "line", x1=str(x), y1=str(y_high), x2=str(x), y2=str(y_low), stroke=fill_color, style="stroke-width: 4;"
    )

    # Body (open-close rectangle)
    y_open = price_to_y(open_price)
    y_close = price_to_y(close)
    body_top = min(y_open, y_close)
    body_height = abs(y_close - y_open)
    # Minimum height for visibility when open == close
    if body_height < 4:
        body_height = 4
        body_top = y_open - 2

    ET.SubElement(
        svg,
        "rect",
        x=str(x - candle_width / 2),
        y=str(body_top),
        width=str(candle_width),
        height=str(body_height),
        fill=fill_color,
        stroke=fill_color,
        style="stroke-width: 2;",
    )

# X-axis labels (every 3rd to avoid overlap)
for i, date in enumerate(dates):
    if i % 3 == 0:
        x = idx_to_x(i)
        x_tick = ET.SubElement(
            svg,
            "text",
            x=str(x),
            y=str(MARGIN_TOP + plot_height + 50),
            fill=TEXT_COLOR,
            style="font-family: sans-serif; font-size: 28px;",
            transform=f"rotate(45, {x}, {MARGIN_TOP + plot_height + 50})",
        )
        x_tick.set("text-anchor", "start")
        x_tick.text = date

# Legend
legend_y = HEIGHT - 100
legend_x = MARGIN_LEFT + 100

# Bullish indicator
ET.SubElement(svg, "rect", x=str(legend_x), y=str(legend_y - 20), width="40", height="30", fill=BULLISH_COLOR)
bullish_text = ET.SubElement(
    svg,
    "text",
    x=str(legend_x + 60),
    y=str(legend_y),
    fill=TEXT_COLOR,
    style="font-family: sans-serif; font-size: 36px;",
)
bullish_text.text = "Bullish (Close ≥ Open)"

# Bearish indicator
legend_x2 = legend_x + 500
ET.SubElement(svg, "rect", x=str(legend_x2), y=str(legend_y - 20), width="40", height="30", fill=BEARISH_COLOR)
bearish_text = ET.SubElement(
    svg,
    "text",
    x=str(legend_x2 + 60),
    y=str(legend_y),
    fill=TEXT_COLOR,
    style="font-family: sans-serif; font-size: 36px;",
)
bearish_text.text = "Bearish (Close < Open)"

# Convert to string
svg_string = ET.tostring(svg, encoding="unicode")

# Save as HTML (SVG embedded)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>candlestick-basic · pygal · pyplots.ai</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
{svg_string}
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)

# Save as PNG using cairosvg
cairosvg.svg2png(bytestring=svg_string.encode(), write_to="plot.png")
