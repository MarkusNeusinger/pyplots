""" pyplots.ai
line-stock-comparison: Stock Price Comparison Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Data - Simulated daily stock prices for ~1 year (252 trading days)
np.random.seed(42)
n_days = 252
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")  # Business days

# Simulate cumulative returns with different trends
returns_aapl = np.random.normal(0.0008, 0.018, n_days)  # Strong growth
returns_googl = np.random.normal(0.0005, 0.020, n_days)  # Moderate growth
returns_msft = np.random.normal(0.0006, 0.016, n_days)  # Steady growth
returns_spy = np.random.normal(0.0004, 0.012, n_days)  # Market benchmark

# Convert to price series (starting at arbitrary prices, then rebase to 100)
price_aapl = 100 * np.cumprod(1 + returns_aapl)
price_googl = 100 * np.cumprod(1 + returns_googl)
price_msft = 100 * np.cumprod(1 + returns_msft)
price_spy = 100 * np.cumprod(1 + returns_spy)

# Rebase all series to 100 at start (already done since we start at 100)
rebased_aapl = price_aapl / price_aapl[0] * 100
rebased_googl = price_googl / price_googl[0] * 100
rebased_msft = price_msft / price_msft[0] * 100
rebased_spy = price_spy / price_spy[0] * 100

# Create custom style with colorblind-friendly palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#0072B2", "#E69F00", "#CC79A7", "#009E73"),  # Colorblind-safe: blue, orange, pink, teal
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=42,
    value_font_size=28,
    value_label_font_size=28,
    tooltip_font_size=32,
    stroke_width=5,
    font_family="sans-serif",
)

# Create line chart with interactive features
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="line-stock-comparison · pygal · pyplots.ai",
    x_title="Date",
    y_title="Rebased Price (Start = 100)",
    show_x_guides=False,
    show_y_guides=True,
    dots_size=2,  # Small dots for interactivity
    stroke_style={"width": 4},
    legend_at_bottom=False,
    legend_box_size=32,
    x_label_rotation=45,
    show_minor_x_labels=False,
    x_labels_major_count=7,  # Show 7 major labels
    show_only_major_dots=True,  # Only show dots at major points
    range=(70, 180),  # Ensure y-axis range includes reference line
)

# Create x-axis labels - show monthly labels
date_labels = []
for i, d in enumerate(dates):
    if i == 0 or d.month != dates[i - 1].month:
        date_labels.append(d.strftime("%b %Y"))
    else:
        date_labels.append("")
chart.x_labels = date_labels

# Create data with custom tooltips for interactivity
data_aapl = [
    {"value": val, "label": f"AAPL | {dates[i].strftime('%Y-%m-%d')} | {val:.1f}"}
    for i, val in enumerate(rebased_aapl.tolist())
]
data_googl = [
    {"value": val, "label": f"GOOGL | {dates[i].strftime('%Y-%m-%d')} | {val:.1f}"}
    for i, val in enumerate(rebased_googl.tolist())
]
data_msft = [
    {"value": val, "label": f"MSFT | {dates[i].strftime('%Y-%m-%d')} | {val:.1f}"}
    for i, val in enumerate(rebased_msft.tolist())
]
data_spy = [
    {"value": val, "label": f"SPY | {dates[i].strftime('%Y-%m-%d')} | {val:.1f}"}
    for i, val in enumerate(rebased_spy.tolist())
]

# Add data series with custom tooltips
chart.add("AAPL", data_aapl)
chart.add("GOOGL", data_googl)
chart.add("MSFT", data_msft)
chart.add("SPY (Benchmark)", data_spy)

# Add horizontal reference line at 100 (starting point)
reference_line = [{"value": 100, "label": "Starting Point (100)"} for _ in range(n_days)]
chart.add("Reference (100)", reference_line, stroke_dasharray="10,5", dots_size=0, stroke_width=3)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
