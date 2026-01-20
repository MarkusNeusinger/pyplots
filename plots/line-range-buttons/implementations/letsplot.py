""" pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-20
"""

import os
import shutil

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()  # noqa: F405

# Data - 2 years of daily stock-like price data
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
n_days = len(dates)

# Generate realistic stock price pattern with trend and volatility
returns = np.random.randn(n_days) * 0.015  # Daily returns with ~1.5% volatility
returns[0] = 0
price = 100 * np.exp(np.cumsum(returns) + np.linspace(0, 0.3, n_days))  # Upward trend

df = pd.DataFrame({"date": dates, "price": price})

# Calculate 1Y range (last 365 days) to highlight as active selection
end_date = dates[-1]
start_1y = end_date - pd.Timedelta(days=365)
df_1y = df[df["date"] >= start_1y].copy()

# Range selector button labels
button_labels = ["1M", "3M", "6M", "YTD", "1Y", "All"]

# Calculate y-position for buttons in data space
price_max = df_1y["price"].max()
price_min = df_1y["price"].min()
price_range = price_max - price_min
button_y = price_max + price_range * 0.12

# Date range for x-positions
date_min = df_1y["date"].min()
date_max = df_1y["date"].max()
date_range_days = (date_max - date_min).days

# Create button positions in data coordinates
button_dates = [
    date_min + pd.Timedelta(days=int(date_range_days * x)) for x in np.linspace(0.12, 0.88, len(button_labels))
]
button_df = pd.DataFrame(
    {
        "date": button_dates,
        "y": [button_y] * len(button_labels),
        "label": button_labels,
        "is_active": ["1Y" == lbl for lbl in button_labels],
    }
)

# Create the plot with range selector buttons
plot = (
    ggplot(df_1y, aes(x="date", y="price"))  # noqa: F405
    + geom_area(fill="#306998", alpha=0.12)  # noqa: F405
    + geom_line(color="#306998", size=1.5)  # noqa: F405
    # Inactive range selector buttons
    + geom_label(  # noqa: F405
        data=button_df[~button_df["is_active"]],
        mapping=aes(x="date", y="y", label="label"),  # noqa: F405
        fill="#F0F0F0",
        color="#306998",
        size=14,
        label_padding=0.6,
    )
    # Active range selector button (1Y highlighted)
    + geom_label(  # noqa: F405
        data=button_df[button_df["is_active"]],
        mapping=aes(x="date", y="y", label="label"),  # noqa: F405
        fill="#306998",
        color="#FFFFFF",
        size=14,
        label_padding=0.6,
        fontface="bold",
    )
    + labs(x="Date", y="Price ($)", title="line-range-buttons · letsplot · pyplots.ai")  # noqa: F405
    + scale_x_datetime(format="%b %Y")  # noqa: F405
    + scale_y_continuous(format="${,.0f}")  # noqa: F405
    + coord_cartesian(ylim=[price_min - price_range * 0.05, price_max + price_range * 0.22])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_text_x=element_text(angle=45),  # noqa: F405
        panel_grid_major=element_line(color="#E0E0E0", size=0.5),  # noqa: F405
        panel_grid_minor=element_line(color="#F0F0F0", size=0.3),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
    + ggtb()  # noqa: F405 - Add interactive pan/zoom toolbar
)

# Save outputs
ggsave(plot, "plot.png", scale=3)  # noqa: F405
ggsave(plot, "plot.html")  # noqa: F405

# lets-plot saves to lets-plot-images subfolder - move files to current directory
if os.path.exists("lets-plot-images/plot.png"):
    shutil.move("lets-plot-images/plot.png", "plot.png")
if os.path.exists("lets-plot-images/plot.html"):
    shutil.move("lets-plot-images/plot.html", "plot.html")
if os.path.exists("lets-plot-images"):
    shutil.rmtree("lets-plot-images")
