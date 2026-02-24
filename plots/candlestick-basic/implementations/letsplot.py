""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 88/100 | Updated: 2026-02-24
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()  # noqa: F405

# Data - simulated 30 trading days of stock OHLC data
np.random.seed(42)
n_days = 30

dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")

# Generate realistic OHLC data with random walk
price = 100.0
opens, highs, lows, closes = [], [], [], []

for _ in range(n_days):
    open_price = price
    change = np.random.randn() * 2
    close_price = open_price + change
    high_price = max(open_price, close_price) + abs(np.random.randn()) * 1.5
    low_price = min(open_price, close_price) - abs(np.random.randn()) * 1.5

    opens.append(open_price)
    closes.append(close_price)
    highs.append(high_price)
    lows.append(low_price)

    price = close_price

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes})

# Candlestick properties
df["bullish"] = df["close"] >= df["open"]
df["body_low"] = df[["open", "close"]].min(axis=1)
df["body_high"] = df[["open", "close"]].max(axis=1)
df["x"] = range(len(df))
df["xmin"] = df["x"] - 0.35
df["xmax"] = df["x"] + 0.35
df["date_str"] = df["date"].dt.strftime("%b %d")

bull_color = "#2271B5"  # Blue for bullish (up)
bear_color = "#D55E00"  # Orange for bearish (down) — colorblind-safe

bull_df = df[df["bullish"]].copy()
bear_df = df[~df["bullish"]].copy()

# Tick label positions: every 5th trading day
tick_pos = list(range(0, n_days, 5))
tick_labels = [dates[i].strftime("%b %d") for i in tick_pos]

# Tooltip template for interactive HTML export
tip_fmt = (
    layer_tooltips()  # noqa: F405
    .line("@date_str")
    .line("Open|$@open")
    .line("High|$@high")
    .line("Low|$@low")
    .line("Close|$@close")
)

# Plot
plot = (
    ggplot()  # noqa: F405
    # Wicks (high-low lines) colored per direction
    + geom_segment(  # noqa: F405
        aes(x="x", xend="x", y="low", yend="high"),  # noqa: F405
        data=bull_df,
        color=bull_color,
        size=0.9,
        tooltips=tip_fmt,
    )
    + geom_segment(  # noqa: F405
        aes(x="x", xend="x", y="low", yend="high"),  # noqa: F405
        data=bear_df,
        color=bear_color,
        size=0.9,
        tooltips=tip_fmt,
    )
    # Bullish candle bodies (blue)
    + geom_rect(  # noqa: F405
        aes(xmin="xmin", xmax="xmax", ymin="body_low", ymax="body_high"),  # noqa: F405
        data=bull_df,
        fill=bull_color,
        color=bull_color,
        size=0.5,
        tooltips=tip_fmt,
    )
    # Bearish candle bodies (orange)
    + geom_rect(  # noqa: F405
        aes(xmin="xmin", xmax="xmax", ymin="body_low", ymax="body_high"),  # noqa: F405
        data=bear_df,
        fill=bear_color,
        color=bear_color,
        size=0.5,
        tooltips=tip_fmt,
    )
    + scale_x_continuous(breaks=tick_pos, labels=tick_labels, expand=[0.02, 0])  # noqa: F405
    + labs(  # noqa: F405
        x="Trading Day (Jan\u2013Feb 2024)", y="Price ($)", title="candlestick-basic \u00b7 letsplot \u00b7 pyplots.ai"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20, color="#333333"),  # noqa: F405
        axis_text=element_text(size=16, color="#555555"),  # noqa: F405
        plot_title=element_text(size=24, color="#222222"),  # noqa: F405
        panel_grid_major_x=element_line(color="#ececec", size=0.3),  # noqa: F405
        panel_grid_major_y=element_line(color="#e0e0e0", size=0.4),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
        axis_ticks=element_blank(),  # noqa: F405
        plot_background=element_rect(fill="white", color="white"),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)  # noqa: F405
ggsave(plot, "plot.html", path=".")  # noqa: F405
