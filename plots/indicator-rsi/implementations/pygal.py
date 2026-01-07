"""pyplots.ai
indicator-rsi: RSI Technical Indicator Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate realistic RSI values over 120 trading days
np.random.seed(42)

# Simulate price changes and calculate RSI
n_days = 120
# Create price changes that lead to realistic RSI patterns
price_changes = np.random.randn(n_days) * 2

# Calculate RSI using exponential moving average
lookback = 14
gains = np.where(price_changes > 0, price_changes, 0)
losses = np.where(price_changes < 0, -price_changes, 0)

# Initialize EMA
avg_gain = np.zeros(n_days)
avg_loss = np.zeros(n_days)

# First average
avg_gain[lookback - 1] = np.mean(gains[:lookback])
avg_loss[lookback - 1] = np.mean(losses[:lookback])

# EMA for subsequent values
alpha = 1 / lookback
for i in range(lookback, n_days):
    avg_gain[i] = alpha * gains[i] + (1 - alpha) * avg_gain[i - 1]
    avg_loss[i] = alpha * losses[i] + (1 - alpha) * avg_loss[i - 1]

# Calculate RSI (avoid division by zero)
with np.errstate(divide="ignore", invalid="ignore"):
    rs = np.divide(avg_gain, avg_loss, out=np.full_like(avg_gain, 100.0), where=avg_loss > 0)
rsi = 100 - (100 / (1 + rs))
rsi[:lookback] = 50  # Fill initial values with neutral


# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#30A030", "#D04040", "#888888"),  # RSI line, oversold, overbought, center
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=5,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="indicator-rsi · pygal · pyplots.ai",
    x_title="Trading Period (120 days, 14-period RSI lookback)",
    y_title="RSI Value (0-100)",
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    stroke_style={"width": 5},
    range=(0, 100),
    interpolate="cubic",
    legend_at_bottom=True,
    legend_box_size=30,
    margin=50,
    margin_bottom=150,
    show_x_labels=False,
)

# Add RSI data
chart.add("RSI (14)", list(rsi))

# Add threshold lines (constant values across all days)
overbought_line = [70] * n_days
oversold_line = [30] * n_days
centerline = [50] * n_days

chart.add("Overbought (70)", overbought_line, stroke_style={"width": 3, "dasharray": "10,5"})
chart.add("Oversold (30)", oversold_line, stroke_style={"width": 3, "dasharray": "10,5"})
chart.add("Centerline (50)", centerline, stroke_style={"width": 2, "dasharray": "5,5"})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
