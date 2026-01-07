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
base_changes = np.random.randn(n_days) * 0.8

# Strong uptrend periods (push RSI above 70)
base_changes[15:32] += 4.0
base_changes[75:92] += 4.5

# Strong downtrend periods (push RSI below 30)
base_changes[40:57] -= 4.0
base_changes[100:115] -= 3.5

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


# Custom style with colorblind-friendly palette (orange/blue instead of red/green)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#FFCCCC",  # Overbought zone fill (light red/pink)
        "#CCFFCC",  # Oversold zone fill (light green)
        "#E67E22",  # Overbought line (orange - colorblind friendly)
        "#3498DB",  # Oversold line (blue - colorblind friendly)
        "#888888",  # Centerline (gray)
        "#306998",  # RSI line (blue)
    ),
    title_font_size=80,
    label_font_size=52,
    major_label_font_size=46,
    legend_font_size=52,
    value_font_size=40,
    stroke_width=6,
    opacity=0.25,
    opacity_hover=0.4,
    guide_stroke_color="#CCCCCC",
    guide_stroke_dasharray="5,5",
)

# Create chart with zone visualization using fill_between simulation
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
    y_labels=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    range=(0, 100),
    interpolate="cubic",
    legend_at_bottom=True,
    legend_box_size=40,
    margin=60,
    margin_bottom=180,
    show_x_labels=False,
    tooltip_fancy_mode=True,
    tooltip_border_radius=10,
)

# Add zone shading by using filled areas
# Overbought zone (70-100): create upper and lower bounds
overbought_upper = [100] * n_days
overbought_lower = [70] * n_days

# Oversold zone (0-30): create upper and lower bounds
oversold_upper = [30] * n_days
oversold_lower = [0] * n_days

# Add overbought zone as filled area (light red/pink background)
chart.add(
    "Overbought Zone (70-100)", overbought_upper, fill=True, stroke_style={"width": 0}, show_dots=False, secondary=True
)

# Add oversold zone as filled area (light green background)
chart.add("Oversold Zone (0-30)", oversold_upper, fill=True, stroke_style={"width": 0}, show_dots=False, secondary=True)

# Add threshold lines with colorblind-friendly colors (orange/blue)
chart.add("Overbought (70)", overbought_lower, stroke_style={"width": 5, "dasharray": "20,10"}, show_dots=False)

chart.add("Oversold (30)", oversold_upper, stroke_style={"width": 5, "dasharray": "20,10"}, show_dots=False)

# Add centerline (gray, dotted)
centerline = [50] * n_days
chart.add("Centerline (50)", centerline, stroke_style={"width": 3, "dasharray": "10,10"}, show_dots=False)

# Add RSI data with enhanced tooltips showing exact values
rsi_data = [{"value": float(v), "label": f"RSI: {v:.1f}"} for v in rsi]
chart.add("RSI (14)", rsi_data, stroke_style={"width": 8}, show_dots=False)

# Save as PNG and HTML (interactive version with tooltips)
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
