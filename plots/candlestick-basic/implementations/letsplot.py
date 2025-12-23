"""pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import cairosvg
import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_rect,
    geom_segment,
    ggplot,
    ggsize,
    labs,
    scale_x_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - simulated 30 trading days of stock OHLC data
np.random.seed(42)
n_days = 30

dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")  # Business days

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

# Calculate candlestick properties
df["bullish"] = df["close"] >= df["open"]
df["color"] = df["bullish"].map({True: "#22C55E", False: "#EF4444"})  # Green/Red
df["body_low"] = df[["open", "close"]].min(axis=1)
df["body_high"] = df[["open", "close"]].max(axis=1)
df["x"] = range(len(df))  # Numeric x for positioning
df["xmin"] = df["x"] - 0.35
df["xmax"] = df["x"] + 0.35

# Plot
plot = (
    ggplot()
    # Wicks (high-low lines)
    + geom_segment(aes(x="x", xend="x", y="low", yend="high"), data=df, color="#666666", size=1)
    # Bullish candle bodies (green)
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="body_low", ymax="body_high"),
        data=df[df["bullish"]],
        fill="#22C55E",
        color="#22C55E",
        size=0.5,
    )
    # Bearish candle bodies (red)
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="body_low", ymax="body_high"),
        data=df[~df["bullish"]],
        fill="#EF4444",
        color="#EF4444",
        size=0.5,
    )
    # Labels and theme
    + scale_x_continuous(
        breaks=list(range(0, n_days, 5)), labels=[df["date"].iloc[i].strftime("%b %d") for i in range(0, n_days, 5)]
    )
    + labs(x="Date", y="Price ($)", title="candlestick-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")

# Save SVG first, then convert to PNG
ggsave(plot, "plot.svg", path=".", w=1600, h=900, unit="px")

# Convert SVG to PNG using cairosvg
with open("plot.svg", "r") as f:
    svg_content = f.read()

cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=4800, output_height=2700)
