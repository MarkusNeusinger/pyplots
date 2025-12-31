"""pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - 60 trading days of synthetic stock data
np.random.seed(42)
n_days = 60
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")

# Generate realistic price movement with trend and volatility
returns = np.random.normal(0.001, 0.02, n_days)
close_prices = 150 * np.cumprod(1 + returns)

# Generate OHLC from close prices
open_prices = np.roll(close_prices, 1)
open_prices[0] = 150
high_prices = np.maximum(open_prices, close_prices) * (1 + np.abs(np.random.normal(0, 0.01, n_days)))
low_prices = np.minimum(open_prices, close_prices) * (1 - np.abs(np.random.normal(0, 0.01, n_days)))

# Generate volume with some correlation to price movement
base_volume = 5_000_000
volatility = np.abs(close_prices - open_prices) / open_prices
volume = base_volume * (1 + volatility * 10 + np.random.uniform(-0.3, 0.3, n_days))
volume = volume.astype(int)

# Determine up/down days for coloring
direction = ["up" if c >= o else "down" for c, o in zip(close_prices, open_prices)]

df = pd.DataFrame(
    {
        "date": dates,
        "date_idx": range(n_days),
        "open": open_prices,
        "high": high_prices,
        "low": low_prices,
        "close": close_prices,
        "volume": volume,
        "direction": direction,
    }
)

# Colors for up/down
color_up = "#22C55E"
color_down = "#EF4444"

# Create candlestick chart (main pane)
candle_plot = (
    ggplot(df)
    # Wicks (high-low lines)
    + geom_segment(aes(x="date_idx", xend="date_idx", y="low", yend="high", color="direction"), size=1.0)
    # Bodies (open-close rectangles)
    + geom_segment(aes(x="date_idx", xend="date_idx", y="open", yend="close", color="direction"), size=5.0)
    + scale_color_manual(values={"up": color_up, "down": color_down})
    + labs(title="candlestick-volume · letsplot · pyplots.ai", y="Price ($)", x="")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title_y=element_text(size=20),
        axis_text_y=element_text(size=16),
        axis_text_x=element_blank(),
        legend_position="none",
        panel_grid_major=element_line(color="#E5E7EB", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 630)
)

# Volume chart (lower pane)
volume_plot = (
    ggplot(df)
    + geom_bar(aes(x="date_idx", y="volume", fill="direction"), stat="identity", width=0.8)
    + scale_fill_manual(values={"up": color_up, "down": color_down})
    + labs(x="Trading Day (Jan-Mar 2024)", y="Volume (M)")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_position="none",
        panel_grid_major=element_line(color="#E5E7EB", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 270)
)

# Use gggrid for dual-pane layout (replaces deprecated GGBunch)
combined = gggrid([candle_plot, volume_plot], ncol=1, heights=[0.7, 0.3])

# Save outputs (path='' ensures files are saved in current directory)
ggsave(combined, "plot.png", scale=3, path=".")
ggsave(combined, "plot.html", path=".")
