""" pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_rect,
    element_text,
    geom_line,
    geom_rect,
    geom_text,
    ggplot,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - 2 years of daily stock-like data
np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=730, freq="D")
returns = np.random.normal(0.0005, 0.02, 730)
price = 100 * np.cumprod(1 + returns)
df = pd.DataFrame({"date": dates, "value": price})

# Calculate ranges for button indicators
end_date = df["date"].max()
ranges = {
    "1M": end_date - pd.DateOffset(months=1),
    "3M": end_date - pd.DateOffset(months=3),
    "6M": end_date - pd.DateOffset(months=6),
    "YTD": pd.Timestamp(f"{end_date.year}-01-01"),
    "1Y": end_date - pd.DateOffset(years=1),
    "All": df["date"].min(),
}

# Create button labels with positions
button_labels = ["1M", "3M", "6M", "YTD", "1Y", "All"]
y_max = df["value"].max()
y_min = df["value"].min()
y_range = y_max - y_min
button_y = y_max + y_range * 0.12

# Button positions (spread across the date range)
start_x = df["date"].min() + pd.DateOffset(days=30)
button_spacing = pd.DateOffset(days=100)
button_positions = [start_x + i * button_spacing for i in range(len(button_labels))]

# Create button data for annotation
buttons_df = pd.DataFrame({"label": button_labels, "x": button_positions, "y": [button_y] * len(button_labels)})

# Mark the "All" button as active (highlighted)
active_button = "All"
buttons_df["is_active"] = buttons_df["label"] == active_button

# Create rectangle data for button backgrounds
rect_width = pd.Timedelta(days=40)
button_rects = pd.DataFrame(
    {
        "xmin": [x - rect_width for x in button_positions],
        "xmax": [x + rect_width for x in button_positions],
        "ymin": [button_y - y_range * 0.04] * len(button_labels),
        "ymax": [button_y + y_range * 0.04] * len(button_labels),
        "is_active": [label == active_button for label in button_labels],
    }
)

# Plot
plot = (
    ggplot(df, aes(x="date", y="value"))
    # Button backgrounds
    + geom_rect(
        data=button_rects[~button_rects["is_active"]],
        mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        fill="#E8E8E8",
        color="#CCCCCC",
        inherit_aes=False,
    )
    + geom_rect(
        data=button_rects[button_rects["is_active"]],
        mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        fill="#306998",
        color="#306998",
        inherit_aes=False,
    )
    # Button labels
    + geom_text(
        data=buttons_df[~buttons_df["is_active"]],
        mapping=aes(x="x", y="y", label="label"),
        color="#333333",
        size=14,
        inherit_aes=False,
    )
    + geom_text(
        data=buttons_df[buttons_df["is_active"]],
        mapping=aes(x="x", y="y", label="label"),
        color="white",
        size=14,
        fontweight="bold",
        inherit_aes=False,
    )
    # Main line
    + geom_line(color="#306998", size=1.5, alpha=0.9)
    # Labels
    + labs(x="Date", y="Price ($)", title="line-range-buttons · plotnine · pyplots.ai")
    # Scales
    + scale_x_datetime(date_breaks="3 months", date_labels="%b %Y")
    + scale_y_continuous(expand=(0.15, 0, 0.05, 0))
    # Theme
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        axis_text_x=element_text(rotation=45, ha="right"),
        panel_grid_minor=element_blank(),
        panel_grid_major=element_text(color="#E0E0E0"),
        plot_background=element_rect(fill="white"),
        panel_background=element_rect(fill="white"),
    )
    # Subtitle annotation
    + annotate(
        "text",
        x=df["date"].min() + pd.DateOffset(days=15),
        y=y_min - y_range * 0.08,
        label="[Static visualization - buttons shown for demonstration]",
        size=10,
        color="#888888",
        ha="left",
    )
)

plot.save("plot.png", dpi=300)
