"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Data - Generate realistic stock price data over 2 years
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=500, freq="B")  # Business days

# Generate realistic stock price using random walk
initial_price = 150.0
returns = np.random.normal(0.0005, 0.02, len(dates))  # Daily returns
prices = initial_price * np.cumprod(1 + returns)

# Create date labels (show monthly for readability)
date_labels = [d.strftime("%b %Y") if d.day <= 5 else "" for d in dates]

# Custom style for large canvas (4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue for primary series
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=32,
    opacity=0.4,  # Semi-transparent fill
    opacity_hover=0.7,
    stroke_width=4,
)

# Create filled line chart (area chart)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="area-stock-range · pygal · pyplots.ai",
    x_title="Date",
    y_title="Price (USD)",
    style=custom_style,
    fill=True,  # Enable area fill
    show_dots=False,  # Hide individual points for cleaner look
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    truncate_label=-1,  # Don't truncate labels
    show_legend=True,
    legend_at_bottom=True,
    show_minor_x_labels=False,
    x_labels_major_every=21,  # Show major label ~monthly
    stroke_style={"width": 4, "linecap": "round", "linejoin": "round"},
    margin=50,
    spacing=30,
)

# Filter date labels for display (show only every ~21 days for monthly view)
filtered_labels = []
for i, _label in enumerate(date_labels):
    if i % 21 == 0:
        filtered_labels.append(dates[i].strftime("%b %Y"))
    else:
        filtered_labels.append("")

chart.x_labels = filtered_labels

# Add stock price data
chart.add("Stock Price", list(prices))

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
