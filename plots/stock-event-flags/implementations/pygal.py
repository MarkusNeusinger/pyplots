"""pyplots.ai
stock-event-flags: Stock Chart with Event Flags
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-21
"""

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Generate stock price data (simulating ~180 trading days)
start_date = pd.Timestamp("2024-01-02")
trading_days = pd.bdate_range(start=start_date, periods=180)

# Generate realistic stock price movement
initial_price = 150.0
returns = np.random.normal(0.0005, 0.018, len(trading_days))
prices = initial_price * np.cumprod(1 + returns)

# Create price dataframe
df = pd.DataFrame({"date": trading_days, "close": prices})

# Define events with their dates, types, and labels
events = [
    {"date": pd.Timestamp("2024-01-25"), "type": "earnings", "label": "Q4 Earnings Beat"},
    {"date": pd.Timestamp("2024-02-15"), "type": "dividend", "label": "Div $0.25"},
    {"date": pd.Timestamp("2024-03-12"), "type": "news", "label": "New Product Launch"},
    {"date": pd.Timestamp("2024-04-18"), "type": "earnings", "label": "Q1 Earnings"},
    {"date": pd.Timestamp("2024-05-10"), "type": "dividend", "label": "Div $0.28"},
    {"date": pd.Timestamp("2024-06-05"), "type": "split", "label": "3:1 Stock Split"},
    {"date": pd.Timestamp("2024-07-22"), "type": "earnings", "label": "Q2 Strong"},
    {"date": pd.Timestamp("2024-08-08"), "type": "dividend", "label": "Div $0.30"},
]

# Event type colors and symbols
event_colors = {"earnings": "#2E86AB", "dividend": "#28A745", "split": "#9B59B6", "news": "#E74C3C"}

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=36,
    stroke_width=4,
    value_label_font_size=32,
    tooltip_font_size=36,
)

# Create the line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="stock-event-flags · pygal · pyplots.ai",
    x_title="Trading Date (2024)",
    y_title="Stock Price ($)",
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    show_dots=False,
    stroke_style={"width": 4},
    fill=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    dots_size=8,
    truncate_label=-1,
    truncate_legend=-1,
    margin=50,
    spacing=30,
)

# Set x-axis labels (show every 20th trading day for readability)
x_labels = []
for i, date in enumerate(df["date"]):
    if i % 20 == 0:
        x_labels.append(date.strftime("%b %d"))
    else:
        x_labels.append("")
chart.x_labels = x_labels

# Add main stock price line
chart.add("Stock Price", list(df["close"]), stroke_style={"width": 4})

# Create event markers as separate series
# We'll add events as point data at their respective positions
for event_type in ["earnings", "dividend", "split", "news"]:
    event_data = [None] * len(df)
    type_events = [e for e in events if e["type"] == event_type]

    for event in type_events:
        # Find the closest trading day
        idx = df["date"].searchsorted(event["date"])
        if idx < len(df):
            # Position the flag above the price
            price_at_event = df.iloc[idx]["close"]
            # Add offset to show flag above price
            flag_position = price_at_event * 1.08
            event_data[idx] = {"value": flag_position, "label": event["label"], "color": event_colors[event_type]}

    # Add series with custom styling
    type_label = event_type.capitalize()

    chart.add(type_label, event_data, dots_size=20, stroke=False, show_dots=True)

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
