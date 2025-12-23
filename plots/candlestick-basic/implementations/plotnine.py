""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_text,
    geom_rect,
    geom_segment,
    ggplot,
    labs,
    scale_fill_manual,
    theme,
    theme_minimal,
)


# Data - 30 trading days of simulated stock prices
np.random.seed(42)
n_days = 30

dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")

# Generate realistic OHLC data with random walk
price = 150.0
opens, highs, lows, closes = [], [], [], []

for _ in range(n_days):
    open_price = price
    # Daily movement: random direction and magnitude
    change = np.random.randn() * 3
    close_price = open_price + change
    # High and low extend beyond open/close
    high_price = max(open_price, close_price) + abs(np.random.randn() * 1.5)
    low_price = min(open_price, close_price) - abs(np.random.randn() * 1.5)

    opens.append(open_price)
    highs.append(high_price)
    lows.append(low_price)
    closes.append(close_price)

    # Next day opens near previous close
    price = close_price + np.random.randn() * 0.5

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes})

# Add columns for plotting
df["date_num"] = np.arange(len(df))
df["direction"] = np.where(df["close"] >= df["open"], "up", "down")
df["body_top"] = df[["open", "close"]].max(axis=1)
df["body_bottom"] = df[["open", "close"]].min(axis=1)

# Plot - build candlestick with segments (wicks) and rectangles (bodies)
plot = (
    ggplot(df)
    # Wicks (high-low lines)
    + geom_segment(aes(x="date_num", xend="date_num", y="low", yend="high"), color="#333333", size=1)
    # Candle bodies (rectangles)
    + geom_rect(
        aes(xmin="date_num - 0.4", xmax="date_num + 0.4", ymin="body_bottom", ymax="body_top", fill="direction")
    )
    # Colors: green for up, red for down
    + scale_fill_manual(values={"up": "#22ab94", "down": "#f23645"}, guide=None)
    + labs(x="Trading Day", y="Price ($)", title="candlestick-basic \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", size=0.5, alpha=0.3),
        panel_grid_minor=element_line(color="#eeeeee", size=0.3, alpha=0.2),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
