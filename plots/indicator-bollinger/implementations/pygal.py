""" pyplots.ai
indicator-bollinger: Bollinger Bands Indicator Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-07
"""

import numpy as np
import pygal
from pygal.style import Style


# Seed for reproducibility
np.random.seed(42)

# Generate realistic stock price data (120 trading days)
n_days = 120
base_price = 150

# Generate price movements with trend and volatility
returns = np.random.normal(0.0005, 0.015, n_days)
prices = base_price * np.cumprod(1 + returns)

# Calculate Bollinger Bands (20-period SMA with 2 standard deviations)
window = 20
sma = np.array([np.mean(prices[max(0, i - window + 1) : i + 1]) if i >= window - 1 else None for i in range(n_days)])
std = np.array([np.std(prices[max(0, i - window + 1) : i + 1]) if i >= window - 1 else None for i in range(n_days)])
upper_band = np.array([sma[i] + 2 * std[i] if sma[i] is not None else None for i in range(n_days)])
lower_band = np.array([sma[i] - 2 * std[i] if sma[i] is not None else None for i in range(n_days)])

# Create x-axis labels (trading days)
x_labels = [f"Day {i + 1}" for i in range(n_days)]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#7EB3D4", "#7EB3D4"),  # Price, SMA, Upper, Lower (bands same color)
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=36,
    legend_font_size=42,
    value_font_size=32,
    tooltip_font_size=28,
    stroke_width=4,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="indicator-bollinger · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Price (USD)",
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    show_dots=False,
    stroke_style={"width": 4},
    legend_at_bottom=True,
    legend_box_size=30,
    truncate_label=10,
    show_minor_x_labels=False,
    x_labels_major_every=20,
    fill=False,
    interpolate="cubic",
    margin=50,
    spacing=30,
)

# Set x labels
chart.x_labels = x_labels

# Add data series - convert to list and handle None values
chart.add("Close Price", prices.tolist(), stroke_style={"width": 5, "dasharray": "0"})
chart.add("SMA (20)", [float(v) if v is not None else None for v in sma], stroke_style={"width": 3, "dasharray": "8,4"})
chart.add("Upper Band", [float(v) if v is not None else None for v in upper_band], stroke_style={"width": 3})
chart.add("Lower Band", [float(v) if v is not None else None for v in lower_band], stroke_style={"width": 3})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
