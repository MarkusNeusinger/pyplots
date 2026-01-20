"""pyplots.ai
dashboard-synchronized-crosshair: Synchronized Multi-Chart Dashboard
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Stock-like data with price, volume, and RSI indicator
np.random.seed(42)
n_points = 200

dates = pd.date_range("2024-01-01", periods=n_points, freq="B")

# Price series (cumulative random walk)
returns = np.random.normal(0.001, 0.02, n_points)
price = 100 * np.cumprod(1 + returns)

# Volume series (correlated with absolute returns)
base_volume = 1000000
volume = base_volume * (1 + 2 * np.abs(returns)) * np.random.uniform(0.8, 1.2, n_points)

# RSI-like indicator (oscillating between 30-70 mostly)
rsi = 50 + 20 * np.sin(np.linspace(0, 8 * np.pi, n_points)) + np.random.normal(0, 5, n_points)
rsi = np.clip(rsi, 0, 100)

df = pd.DataFrame(
    {
        "date": dates,
        "price": price,
        "volume": volume / 1e6,  # In millions
        "rsi": rsi,
    }
)

# Common theme for all charts
common_theme = theme(  # noqa: F405
    axis_title=element_text(size=18),  # noqa: F405
    axis_text=element_text(size=14),  # noqa: F405
    plot_title=element_text(size=20),  # noqa: F405
    legend_text=element_text(size=14),  # noqa: F405
    axis_line=element_line(size=1),  # noqa: F405
    panel_grid_major=element_line(color="#E0E0E0", size=0.5),  # noqa: F405
    panel_grid_minor=element_blank(),  # noqa: F405
)

# Chart 1: Price
price_chart = (
    ggplot(df, aes(x="date", y="price"))  # noqa: F405
    + geom_line(color="#306998", size=1.5)  # noqa: F405
    + labs(x="", y="Price ($)", title="Price")  # noqa: F405
    + theme_minimal()  # noqa: F405
    + common_theme
)

# Chart 2: Volume
volume_chart = (
    ggplot(df, aes(x="date", y="volume"))  # noqa: F405
    + geom_bar(stat="identity", fill="#FFD43B", alpha=0.8, width=0.8)  # noqa: F405
    + labs(x="", y="Volume (M)", title="Volume")  # noqa: F405
    + theme_minimal()  # noqa: F405
    + common_theme
)

# Chart 3: RSI Indicator
rsi_chart = (
    ggplot(df, aes(x="date", y="rsi"))  # noqa: F405
    + geom_line(color="#DC2626", size=1.5)  # noqa: F405
    + geom_hline(yintercept=70, linetype="dashed", color="#888888", size=0.8)  # noqa: F405
    + geom_hline(yintercept=30, linetype="dashed", color="#888888", size=0.8)  # noqa: F405
    + labs(x="Date", y="RSI", title="RSI Indicator")  # noqa: F405
    + scale_y_continuous(limits=[0, 100])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + common_theme
)

# Combine charts using gggrid for vertical stacked layout
combined = (
    gggrid([price_chart, volume_chart, rsi_chart], ncol=1, heights=[1, 1, 1])  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + ggtitle("dashboard-synchronized-crosshair · letsplot · pyplots.ai")  # noqa: F405
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(combined, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(combined, filename="plot.html", path=".")
