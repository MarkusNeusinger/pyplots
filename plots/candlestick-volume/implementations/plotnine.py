"""pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-01
"""

import os
import warnings

import numpy as np
import pandas as pd
from PIL import Image
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_col,
    geom_rect,
    geom_segment,
    ggplot,
    guides,
    labs,
    scale_color_manual,
    scale_fill_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)


warnings.filterwarnings("ignore")

# Data - Generate realistic stock OHLC data with volume
np.random.seed(42)
n_days = 60

# Start with a base price and generate realistic price movements
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")
base_price = 150.0
returns = np.random.normal(0.001, 0.02, n_days)
close_prices = base_price * np.cumprod(1 + returns)

# Generate OHLC data with realistic intraday movement
open_prices = np.zeros(n_days)
high_prices = np.zeros(n_days)
low_prices = np.zeros(n_days)
open_prices[0] = base_price

for i in range(n_days):
    if i > 0:
        # Open is near previous close with small gap
        gap = np.random.normal(0, 0.003) * close_prices[i - 1]
        open_prices[i] = close_prices[i - 1] + gap

    # Intraday range
    intraday_range = abs(np.random.normal(0.015, 0.008)) * open_prices[i]
    if close_prices[i] >= open_prices[i]:
        # Bullish day
        low_prices[i] = min(open_prices[i], close_prices[i]) - np.random.uniform(0, intraday_range * 0.5)
        high_prices[i] = max(open_prices[i], close_prices[i]) + np.random.uniform(0, intraday_range * 0.5)
    else:
        # Bearish day
        low_prices[i] = min(open_prices[i], close_prices[i]) - np.random.uniform(0, intraday_range * 0.5)
        high_prices[i] = max(open_prices[i], close_prices[i]) + np.random.uniform(0, intraday_range * 0.5)

# Generate volume with correlation to price movement
base_volume = 5_000_000
volume_volatility = abs(close_prices - open_prices) / open_prices
volumes = base_volume * (1 + volume_volatility * 5 + np.random.uniform(-0.3, 0.3, n_days))
volumes = volumes.astype(int)

# Create DataFrame
df = pd.DataFrame(
    {
        "date": dates,
        "day": range(n_days),
        "open": open_prices,
        "high": high_prices,
        "low": low_prices,
        "close": close_prices,
        "volume": volumes,
    }
)

# Determine direction (bullish/bearish)
df["direction"] = np.where(df["close"] >= df["open"], "Bullish", "Bearish")

# Candlestick body boundaries
df["body_bottom"] = df[["open", "close"]].min(axis=1)
df["body_top"] = df[["open", "close"]].max(axis=1)

# Candle width
candle_width = 0.35

# Prepare data for rectangles
df["xmin"] = df["day"] - candle_width
df["xmax"] = df["day"] + candle_width

# Colors: Python Blue for bullish, contrasting red for bearish
color_up = "#306998"
color_down = "#C44E52"

# Date labels for x-axis
x_breaks = [0, 14, 29, 44, 59]
x_labels = ["Jan 02", "Jan 22", "Feb 12", "Mar 04", "Mar 25"]

# Create price candlestick chart
price_plot = (
    ggplot(df, aes(x="day"))
    # Wicks (high-low lines) - draw first so bodies are on top
    + geom_segment(aes(x="day", xend="day", y="low", yend="high", color="direction"), size=1.2)
    # Candlestick bodies using geom_rect
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="body_bottom", ymax="body_top", fill="direction"), color="#333333", size=0.3
    )
    + scale_fill_manual(values={"Bullish": color_up, "Bearish": color_down}, name="Direction")
    + scale_color_manual(values={"Bullish": color_up, "Bearish": color_down})
    + guides(color=None)  # Hide color legend, keep fill legend
    + scale_x_continuous(breaks=x_breaks, labels=x_labels, expand=(0.02, 0.02))
    + labs(x="", y="Price (USD)", title="candlestick-volume · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 6.75),
        text=element_text(size=14),
        axis_title_y=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24, ha="center"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="top",
        legend_direction="horizontal",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#CCCCCC", size=0.5, alpha=0.5),
        axis_text_x=element_blank(),
        axis_ticks_major_x=element_blank(),
        plot_margin=0,
    )
)

# Create volume bar chart
volume_plot = (
    ggplot(df, aes(x="day", y="volume / 1e6", fill="direction"))
    + geom_col(width=candle_width * 2, color="#333333", size=0.2)
    + scale_fill_manual(values={"Bullish": color_up, "Bearish": color_down})
    + guides(fill=None)  # Hide legend on volume chart
    + scale_x_continuous(breaks=x_breaks, labels=x_labels, expand=(0.02, 0.02))
    + labs(x="Date (2024)", y="Volume (M)")
    + theme_minimal()
    + theme(
        figure_size=(16, 2.25),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_position="none",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#CCCCCC", size=0.5, alpha=0.5),
        plot_margin=0,
    )
)

# Combine plots using PIL (plotnine doesn't support multi-panel with different y-scales)
# Save individual plotnine plots then combine as images
price_plot.save("_price_temp.png", dpi=300, verbose=False)
volume_plot.save("_volume_temp.png", dpi=300, verbose=False)

img_price = Image.open("_price_temp.png")
img_volume = Image.open("_volume_temp.png")

# Create combined image with proper aspect ratio
total_height = img_price.height + img_volume.height
combined = Image.new("RGB", (img_price.width, total_height), "white")
combined.paste(img_price, (0, 0))
combined.paste(img_volume, (0, img_price.height))
combined.save("plot.png")

# Clean up temp files
os.remove("_price_temp.png")
os.remove("_volume_temp.png")
