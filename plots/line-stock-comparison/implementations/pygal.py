"""pyplots.ai
line-stock-comparison: Stock Price Comparison Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-20
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

# Create custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C", "#2ECC71"),  # Python blue, yellow, red, green
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=24,
    stroke_width=5,
    font_family="sans-serif",
)

# Create line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="line-stock-comparison · pygal · pyplots.ai",
    x_title="Date",
    y_title="Rebased Price (Start = 100)",
    show_x_guides=False,
    show_y_guides=True,
    dots_size=0,  # Hide individual dots for cleaner lines
    stroke_style={"width": 4},
    legend_at_bottom=False,
    legend_box_size=24,
    truncate_legend=-1,  # Don't truncate legend text
    x_label_rotation=45,
    show_minor_x_labels=False,
)

# Format dates for x-axis labels (show every ~40 trading days for readability)
date_labels = [d.strftime("%b %Y") if i % 40 == 0 else "" for i, d in enumerate(dates)]
chart.x_labels = date_labels

# Add data series
chart.add("AAPL", rebased_aapl.tolist())
chart.add("GOOGL", rebased_googl.tolist())
chart.add("MSFT", rebased_msft.tolist())
chart.add("SPY (Benchmark)", rebased_spy.tolist())

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
