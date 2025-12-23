"""pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Generate 30 trading days of OHLC data
np.random.seed(42)
n_days = 30
start_price = 150.0
dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")

# Generate realistic price movements
returns = np.random.randn(n_days) * 0.02  # 2% daily volatility
prices = start_price * np.cumprod(1 + returns)

# Generate OHLC data
open_prices = []
high_prices = []
low_prices = []
close_prices = []

for i, close in enumerate(prices):
    if i == 0:
        open_price = start_price
    else:
        open_price = close_prices[-1]

    # Generate intraday range
    daily_range = abs(np.random.randn()) * 0.015 * close
    high = max(open_price, close) + daily_range
    low = min(open_price, close) - daily_range

    open_prices.append(open_price)
    high_prices.append(high)
    low_prices.append(low)
    close_prices.append(close)

df = pd.DataFrame({"date": dates, "open": open_prices, "high": high_prices, "low": low_prices, "close": close_prices})

# Determine if bullish (close > open) or bearish
df["bullish"] = df["close"] >= df["open"]

# Create ColumnDataSource
source = ColumnDataSource(df)

# Separate sources for bullish and bearish candles
bullish_df = df[df["bullish"]].copy()
bearish_df = df[~df["bullish"]].copy()
source_bullish = ColumnDataSource(bullish_df)
source_bearish = ColumnDataSource(bearish_df)

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    x_axis_type="datetime",
    title="candlestick-basic · bokeh · pyplots.ai",
    x_axis_label="Date",
    y_axis_label="Price ($)",
    tools="",
    toolbar_location=None,
)

# Candle width in milliseconds (80% of one day)
candle_width = 0.8 * 24 * 60 * 60 * 1000

# Draw wicks (high-low lines) using segment glyph
p.segment(x0="date", y0="high", x1="date", y1="low", source=source, color="#333333", line_width=3)

# Draw bullish candle bodies (green)
p.vbar(
    x="date",
    top="close",
    bottom="open",
    width=candle_width,
    source=source_bullish,
    fill_color="#22c55e",
    line_color="#16a34a",
    line_width=2,
)

# Draw bearish candle bodies (red)
p.vbar(
    x="date",
    top="open",
    bottom="close",
    width=candle_width,
    source=source_bearish,
    fill_color="#ef4444",
    line_color="#dc2626",
    line_width=2,
)

# Styling for 4800x2700 px
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling (subtle)
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Remove minor ticks
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None

# Background
p.background_fill_color = "#ffffff"
p.border_fill_color = "#ffffff"

# Axis styling
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
save(p, filename="plot.html", title="candlestick-basic · bokeh · pyplots.ai")
