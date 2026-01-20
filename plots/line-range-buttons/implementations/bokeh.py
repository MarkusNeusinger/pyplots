"""pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource, CustomJS, DatetimeTickFormatter, HoverTool, Range1d, Row
from bokeh.plotting import figure


# Data - 3 years of daily stock-like data
np.random.seed(42)
start_date = pd.Timestamp("2022-01-01")
end_date = pd.Timestamp("2025-01-01")
dates = pd.date_range(start=start_date, end=end_date, freq="D")
n_points = len(dates)

# Generate realistic price movement (random walk with drift)
returns = np.random.normal(0.0003, 0.015, n_points)
prices = 100 * np.exp(np.cumsum(returns))

df = pd.DataFrame({"date": dates, "value": prices})
source = ColumnDataSource(df)

# Create main figure
p = figure(
    width=4800,
    height=2500,
    title="line-range-buttons · bokeh · pyplots.ai",
    x_axis_type="datetime",
    x_axis_label="Date",
    y_axis_label="Price ($)",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Style the figure
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Line plot - thicker line for visibility
p.line("date", "value", source=source, line_width=4, color="#306998", legend_label="Daily Price")

# Add hover tool
hover = HoverTool(
    tooltips=[("Date", "@date{%F}"), ("Price", "$@value{0.00}")], formatters={"@date": "datetime"}, mode="vline"
)
p.add_tools(hover)

# Style legend
p.legend.label_text_font_size = "22pt"
p.legend.location = "top_left"
p.legend.background_fill_alpha = 0.7

# Date formatter
p.xaxis.formatter = DatetimeTickFormatter(days="%b %d", months="%b %Y", years="%Y")

# Store initial range
initial_start = df["date"].min()
initial_end = df["date"].max()

# Set x_range to a Range1d for JS manipulation
p.x_range = Range1d(start=initial_start, end=initial_end)

# Calculate date ranges for buttons
all_dates = df["date"]
latest_date = all_dates.max()

ranges = {
    "1M": latest_date - pd.DateOffset(months=1),
    "3M": latest_date - pd.DateOffset(months=3),
    "6M": latest_date - pd.DateOffset(months=6),
    "YTD": pd.Timestamp(f"{latest_date.year}-01-01"),
    "1Y": latest_date - pd.DateOffset(years=1),
    "All": all_dates.min(),
}

# Convert to timestamps for JS
range_starts = {k: int(v.timestamp() * 1000) for k, v in ranges.items()}
range_end = int(latest_date.timestamp() * 1000)

# Create buttons with callbacks
buttons = []
button_labels = ["1M", "3M", "6M", "YTD", "1Y", "All"]

for label in button_labels:
    btn = Button(label=label, width=300, height=100, button_type="default" if label != "All" else "primary")

    # JavaScript callback to update range
    callback = CustomJS(
        args={
            "x_range": p.x_range,
            "range_start": range_starts[label],
            "range_end": range_end,
            "buttons": buttons,
            "current_btn": btn,
        },
        code="""
        x_range.start = range_start;
        x_range.end = range_end;

        // Update button styles
        for (let b of buttons) {
            b.button_type = 'default';
        }
        current_btn.button_type = 'primary';
        """,
    )
    btn.js_on_click(callback)
    buttons.append(btn)

# Update the button references in all callbacks
for btn in buttons:
    for cb in btn.js_property_callbacks.get("button_click", []):
        cb.args["buttons"] = buttons

# Button row
button_row = Row(*buttons, spacing=30)

# Layout with explicit dimensions
layout = column(button_row, p, width=4800, height=2700)

# Save outputs
export_png(layout, filename="plot.png")
output_file("plot.html", title="Line Chart with Range Selector Buttons")
save(layout)
