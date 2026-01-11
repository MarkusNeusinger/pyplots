""" pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_area,
    geom_line,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Generate realistic stock price data (2 years of daily prices)
np.random.seed(42)
n_days = 504  # ~2 years of trading days

dates = pd.date_range(start="2024-01-01", periods=n_days, freq="B")  # Business days

# Generate realistic price movements using geometric Brownian motion
initial_price = 150.0
drift = 0.0003  # Daily drift
volatility = 0.018  # Daily volatility
returns = np.random.normal(drift, volatility, n_days)
prices = initial_price * np.cumprod(1 + returns)

# Add some trend and patterns
trend = np.linspace(0, 30, n_days)
seasonal = 10 * np.sin(np.linspace(0, 4 * np.pi, n_days))
prices = prices + trend + seasonal

# Create main DataFrame
df = pd.DataFrame({"date": dates, "price": prices})

# Create a selected range for visualization (last 6 months)
range_end = dates[-1]
range_start = dates[-126]  # ~6 months of trading days
df_selected = df[(df["date"] >= range_start) & (df["date"] <= range_end)].copy()

# Calculate y-axis limits with padding for better visualization
price_min = df_selected["price"].min()
price_max = df_selected["price"].max()
price_range = price_max - price_min
y_min = price_min - price_range * 0.1
y_max = price_max + price_range * 0.1

# Main area chart for selected range
main_chart = (
    ggplot(df_selected, aes(x="date", y="price"))
    + geom_area(fill="#306998", alpha=0.4)
    + geom_line(color="#306998", size=1.5)
    + labs(x="Date", y="Price (USD)", title="Stock Price History (6M Range) · area-stock-range · letsplot · pyplots.ai")
    + scale_x_datetime()
    + scale_y_continuous(limits=[y_min, y_max])
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#cccccc", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save the plot (path='.' to output in current directory)
ggsave(main_chart, "plot.png", path=".", scale=3)

# Also save HTML version for interactivity
ggsave(main_chart, "plot.html", path=".")
