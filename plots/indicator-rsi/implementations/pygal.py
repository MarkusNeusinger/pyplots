"""pyplots.ai
indicator-rsi: RSI Technical Indicator Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-07
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate realistic RSI values over 120 trading days
np.random.seed(42)

n_days = 120
lookback = 14

# Generate price changes that produce RSI entering both overbought (>70) and oversold (<30) zones
# Create trending periods to get extreme RSI values
base_changes = np.random.randn(n_days) * 1.5

# Add trending segments to push RSI into extreme zones
# Strong uptrend periods (push RSI above 70)
base_changes[20:35] += 2.5  # Bullish phase
base_changes[80:95] += 2.8  # Another bullish phase

# Strong downtrend periods (push RSI below 30)
base_changes[45:60] -= 2.5  # Bearish phase
base_changes[105:115] -= 2.2  # Another bearish phase

price_changes = base_changes

# Calculate RSI using exponential moving average
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


# Custom style for large canvas with zone colors
# Series order: Overbought zone, Oversold zone, Overbought line, Oversold line, Centerline, RSI
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#FFCCCC",  # Overbought zone fill (light red)
        "#CCFFCC",  # Oversold zone fill (light green)
        "#D04040",  # Overbought line (red)
        "#30A030",  # Oversold line (green)
        "#888888",  # Centerline (gray)
        "#306998",  # RSI line (blue)
    ),
    title_font_size=80,
    label_font_size=52,
    major_label_font_size=46,
    legend_font_size=52,
    value_font_size=40,
    stroke_width=6,
    opacity=0.95,
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
    stroke_style={"width": 6},
    range=(0, 100),
    interpolate="cubic",
    legend_at_bottom=True,
    legend_box_size=40,
    margin=60,
    margin_bottom=180,
    show_x_labels=False,
)

# Add zone shading for overbought (70-100) and oversold (0-30) zones
# Overbought zone (70-100) - light red fill
overbought_zone = [100] * n_days
chart.add(
    "Overbought Zone (70-100)", overbought_zone, fill=True, secondary=False, stroke_style={"width": 0}, show_dots=False
)

# Oversold zone (0-30) - light green fill
oversold_zone = [30] * n_days
chart.add("Oversold Zone (0-30)", oversold_zone, fill=True, secondary=False, stroke_style={"width": 0}, show_dots=False)

# Add threshold lines (constant values across all days) - thicker for visibility
overbought_line = [70] * n_days
oversold_line = [30] * n_days
centerline = [50] * n_days

chart.add("Overbought (70)", overbought_line, stroke_style={"width": 4, "dasharray": "15,8"})
chart.add("Oversold (30)", oversold_line, stroke_style={"width": 4, "dasharray": "15,8"})
chart.add("Centerline (50)", centerline, stroke_style={"width": 3, "dasharray": "8,8"})

# Add RSI data last so it appears on top
chart.add("RSI (14)", list(rsi), stroke_style={"width": 7})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
