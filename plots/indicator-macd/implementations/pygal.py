""" pyplots.ai
indicator-macd: MACD Technical Indicator Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 83/100 | Created: 2026-01-07
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Data - Generate MACD data from simulated stock prices
np.random.seed(42)

# Generate 150 days of simulated price data with a trend
n_days = 150
dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
price = 100 + np.cumsum(np.random.randn(n_days) * 2 + 0.05)

# Calculate EMAs for MACD (12, 26, 9)
price_series = pd.Series(price)
ema_12 = price_series.ewm(span=12, adjust=False).mean().values
ema_26 = price_series.ewm(span=26, adjust=False).mean().values

# MACD line = 12-day EMA - 26-day EMA
macd_line = ema_12 - ema_26

# Signal line = 9-day EMA of MACD
macd_series = pd.Series(macd_line)
signal_line = macd_series.ewm(span=9, adjust=False).mean().values

# Histogram = MACD - Signal
histogram = macd_line - signal_line

# Use last 100 periods for clearer visualization
start_idx = 50
dates = dates[start_idx:]
macd_line = macd_line[start_idx:]
signal_line = signal_line[start_idx:]
histogram = histogram[start_idx:]

# Custom style for 4800x2700 canvas with distinct colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    # Colors: hist+, hist-, MACD line, Signal line, zero line
    colors=("#2CA02C", "#D62728", "#306998", "#FF7F0E", "#333333"),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=40,
    value_font_size=32,
    tooltip_font_size=28,
    stroke_width=6,
)

# Create Bar chart for histogram bars
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title="indicator-macd · pygal · pyplots.ai",
    x_title="Date",
    y_title="MACD Value",
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    legend_at_bottom=True,
    legend_box_size=30,
    margin=50,
    spacing=0,
)

# Format dates for x-axis labels (show every 15th date to reduce crowding)
date_labels = [d.strftime("%b %d") if i % 15 == 0 else "" for i, d in enumerate(dates)]
chart.x_labels = date_labels

# Add histogram as discrete bars with color per value
# Use None for values of wrong sign to create discrete colored bars
hist_positive = [{"value": h, "color": "#2CA02C"} if h >= 0 else None for h in histogram]
hist_negative = [{"value": h, "color": "#D62728"} if h < 0 else None for h in histogram]

chart.add("Histogram (+)", hist_positive)
chart.add("Histogram (-)", hist_negative)

# Add MACD and Signal lines as secondary series (stroke only, no fill)
# Using explicit stroke configuration to avoid fill
chart.add(
    "MACD (12,26)", list(macd_line), stroke=True, show_dots=False, fill=False, secondary=True, stroke_style={"width": 6}
)
chart.add(
    "Signal (9)", list(signal_line), stroke=True, show_dots=False, fill=False, secondary=True, stroke_style={"width": 6}
)

# Add zero reference line (dashed)
zero_line = [0] * len(macd_line)
chart.add("Zero", zero_line, stroke=True, show_dots=False, fill=False, stroke_style={"width": 3, "dasharray": "10, 5"})

# Save as PNG
chart.render_to_png("plot.png")
