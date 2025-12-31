""" pyplots.ai
line-annotated-events: Annotated Line Plot with Event Markers
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Stock price over a year with quarterly events
np.random.seed(42)
n_days = 250  # Trading days in a year

# Generate realistic stock-like price data with trend
base_price = 150
returns = np.random.randn(n_days) * 0.012
prices = base_price * np.cumprod(1 + returns)

# Create month labels for x-axis
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
x_labels = []
for i in range(n_days):
    if i % 21 == 0:  # Approx monthly
        month_idx = min(i // 21, 11)
        x_labels.append(months[month_idx])
    else:
        x_labels.append("")

# Event data - indices and labels (quarterly earnings + product launch)
events = [(31, "Q4 Earnings"), (94, "Q1 Earnings"), (136, "Launch"), (157, "Q2 Earnings"), (220, "Q3 Earnings")]

# Custom style for 4800x2700 canvas with large fonts
# Use distinct colors: blue for price line, different colors for each event
event_colors = ("#E74C3C", "#F39C12", "#9B59B6", "#27AE60", "#3498DB")
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=("#306998",) + event_colors,
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=32,
    value_label_font_size=28,
    tooltip_font_size=28,
    stroke_width=5,
    font_family="sans-serif",
)

# Create line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="line-annotated-events · pygal · pyplots.ai",
    x_title="Date (2024)",
    y_title="Stock Price (USD)",
    show_dots=False,
    stroke_style={"width": 5, "linecap": "round"},
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    show_x_guides=False,
    show_y_guides=True,
    truncate_label=-1,
    x_label_rotation=0,
    margin=80,
    margin_bottom=180,
    margin_left=160,
    print_values=False,
    interpolate="cubic",
)

# Set x-axis labels
chart.x_labels = x_labels

# Add main stock price line
chart.add("Stock Price", list(prices), stroke_style={"width": 5})

# Add each event as a separate series with its own printed label
# This ensures each event has a visible text annotation on the static PNG
for idx, label in events:
    # Create sparse series with only this event point
    event_series = [None] * n_days
    event_series[idx] = prices[idx]
    chart.add(
        label,
        event_series,
        stroke=False,
        show_dots=True,
        dots_size=22,
        print_values=True,
        print_values_position="top",
        formatter=lambda x, lbl=label: lbl,
    )

# Render outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
