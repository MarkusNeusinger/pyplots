""" pyplots.ai
indicator-macd: MACD Technical Indicator Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-07
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
def calc_ema(data, span):
    return pd.Series(data).ewm(span=span, adjust=False).mean().values


ema_12 = calc_ema(price, 12)
ema_26 = calc_ema(price, 26)

# MACD line = 12-day EMA - 26-day EMA
macd_line = ema_12 - ema_26

# Signal line = 9-day EMA of MACD
signal_line = calc_ema(macd_line, 9)

# Histogram = MACD - Signal
histogram = macd_line - signal_line

# Use last 100 periods for clearer visualization
start_idx = 50
dates = dates[start_idx:]
macd_line = macd_line[start_idx:]
signal_line = signal_line[start_idx:]
histogram = histogram[start_idx:]

# Format dates for x-axis labels (show every 10th date)
date_labels = [d.strftime("%b %d") if i % 10 == 0 else "" for i, d in enumerate(dates)]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FF7F0E", "#2CA02C", "#D62728"),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=40,
    value_font_size=32,
    tooltip_font_size=28,
    stroke_width=5,
)

# Create line chart for MACD and Signal lines
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="indicator-macd · pygal · pyplots.ai",
    x_title="Date",
    y_title="MACD Value",
    show_dots=False,
    stroke_style={"width": 5},
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    legend_at_bottom=True,
    legend_box_size=30,
    truncate_label=10,
    margin=50,
    spacing=20,
)

# Add x-axis labels
chart.x_labels = date_labels

# Add MACD line (blue)
chart.add("MACD (12,26)", list(macd_line), stroke_style={"width": 5})

# Add Signal line (orange)
chart.add("Signal (9)", list(signal_line), stroke_style={"width": 5})

# Add histogram as secondary chart
# For pygal, we'll add histogram values and style them
# Create positive and negative histogram series
hist_positive = [h if h >= 0 else None for h in histogram]
hist_negative = [h if h < 0 else None for h in histogram]

chart.add("Histogram (+)", hist_positive, stroke_style={"width": 2}, fill=True)
chart.add("Histogram (-)", hist_negative, stroke_style={"width": 2}, fill=True)

# Add zero line reference
zero_line = [0] * len(macd_line)
chart.add("Zero", zero_line, stroke_style={"width": 2, "dasharray": "10, 5"}, show_dots=False)

# Save as PNG
chart.render_to_png("plot.png")

# Also save as HTML for interactive view
chart.render_to_file("plot.html")
