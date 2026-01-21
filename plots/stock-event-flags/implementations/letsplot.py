""" pyplots.ai
stock-event-flags: Stock Chart with Event Flags
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-21
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_line,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Generate stock price data (simulating ~180 trading days)
np.random.seed(42)
n_days = 180
dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")

# Generate realistic stock price movement (random walk with drift)
returns = np.random.normal(0.0005, 0.018, n_days)
close_prices = 150 * np.cumprod(1 + returns)

# Create price dataframe
df_price = pd.DataFrame({"date": dates, "close": close_prices})
df_price["date_num"] = np.arange(n_days)

# Define event data with different types
events = [
    {"date": "2024-01-25", "type": "Earnings", "label": "Q4 Earnings Beat"},
    {"date": "2024-02-15", "type": "Dividend", "label": "Dividend $0.25"},
    {"date": "2024-03-20", "type": "News", "label": "Product Launch"},
    {"date": "2024-04-25", "type": "Earnings", "label": "Q1 Earnings"},
    {"date": "2024-05-10", "type": "Dividend", "label": "Dividend $0.25"},
    {"date": "2024-06-05", "type": "News", "label": "Analyst Upgrade"},
    {"date": "2024-07-25", "type": "Earnings", "label": "Q2 Earnings Miss"},
    {"date": "2024-08-15", "type": "Dividend", "label": "Dividend $0.28"},
    {"date": "2024-09-12", "type": "Split", "label": "2:1 Stock Split"},
]

df_events = pd.DataFrame(events)
df_events["date"] = pd.to_datetime(df_events["date"])

# Find matching prices and positions for events
event_prices = []
event_date_nums = []
for event_date in df_events["date"]:
    # Find closest trading day
    idx = np.abs(df_price["date"] - event_date).argmin()
    event_prices.append(df_price.iloc[idx]["close"])
    event_date_nums.append(df_price.iloc[idx]["date_num"])

df_events["price"] = event_prices
df_events["date_num"] = event_date_nums

# Calculate flag positions (alternating heights above price)
price_range = close_prices.max() - close_prices.min()
flag_offsets = []
for i, price in enumerate(event_prices):
    offset = price_range * (0.15 + 0.08 * (i % 3))
    flag_offsets.append(price + offset)

df_events["flag_y"] = flag_offsets

# Color mapping for event types
color_map = {"Earnings": "#306998", "Dividend": "#22C55E", "News": "#F59E0B", "Split": "#DC2626"}
df_events["color"] = df_events["type"].map(color_map)

# Build the plot
plot = (
    ggplot()
    # Stock price line
    + geom_line(aes(x="date_num", y="close"), data=df_price, color="#306998", size=1.2, alpha=0.9)
    # Vertical connector lines from flags to price
    + geom_segment(
        aes(x="date_num", y="price", xend="date_num", yend="flag_y"),
        data=df_events,
        color="#666666",
        size=0.8,
        linetype="dashed",
    )
    # Flag markers (points at flag position)
    + geom_point(
        aes(x="date_num", y="flag_y", color="type"),
        data=df_events,
        size=8,
        shape=18,  # Diamond shape
    )
    # Event labels
    + geom_text(aes(x="date_num", y="flag_y", label="label"), data=df_events, vjust=-1.2, size=10, color="#333333")
    # Price markers at event dates
    + geom_point(aes(x="date_num", y="price"), data=df_events, color="#333333", size=3)
    # Custom colors for event types
    + scale_color_manual(values=["#306998", "#22C55E", "#F59E0B", "#DC2626"], name="Event Type")
    # Labels and title
    + labs(
        x="Trading Days",
        y="Stock Price ($)",
        title="Tech Stock 2024 \u00b7 stock-event-flags \u00b7 letsplot \u00b7 pyplots.ai",
    )
    # Theme
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
