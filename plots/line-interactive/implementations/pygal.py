""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Data - Daily temperature readings for a weather station
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")

# Generate realistic temperature pattern with seasonal variation
day_of_year = np.arange(365)
base_temp = 15 + 12 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Seasonal pattern
noise = np.random.randn(365) * 3  # Daily variation
temperature = base_temp + noise

# Format dates for labels
date_labels = [d.strftime("%b %d") for d in dates]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=4,
    opacity=".9",
    opacity_hover=".95",
    transition="400ms ease-in",
    tooltip_font_size=36,
    value_label_font_size=36,
)

# Create interactive line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="Daily Temperature 2024 · line-interactive · pygal · pyplots.ai",
    x_title="Date",
    y_title="Temperature (°C)",
    show_dots=True,
    dots_size=6,
    stroke_style={"width": 4, "linecap": "round", "linejoin": "round"},
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    truncate_label=12,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=1,
    margin=60,
    spacing=40,
    x_labels_major_every=30,  # Show label every 30 days
    show_minor_x_labels=False,
    tooltip_border_radius=10,
    js=[],  # Enable default JS for interactivity
)

# Add x-axis labels (show every 30 days for readability)
chart.x_labels = date_labels

# Add temperature data
chart.add(
    "Temperature", [{"value": float(t), "label": f"{date_labels[i]}: {t:.1f}°C"} for i, t in enumerate(temperature)]
)

# Save as PNG and HTML (interactive)
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
