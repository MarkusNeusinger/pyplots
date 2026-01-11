""" pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_area,
    geom_line,
    ggplot,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - 2 years of simulated stock price data
np.random.seed(42)
n_days = 500  # ~2 years of trading days
dates = pd.date_range("2022-01-03", periods=n_days, freq="B")  # Business days

# Generate realistic stock price with trends and volatility
initial_price = 150.0
daily_returns = np.random.normal(0.0003, 0.015, n_days)

# Add some trend changes for interesting patterns
trend = np.zeros(n_days)
trend[0:100] = 0.001  # Bull run
trend[100:200] = -0.0008  # Correction
trend[200:350] = 0.0005  # Recovery
trend[350:420] = -0.0003  # Sideways/slight decline
trend[420:] = 0.0008  # Late rally

# Add volatility clusters
volatility_multiplier = np.ones(n_days)
volatility_multiplier[80:120] = 1.8  # High volatility period
volatility_multiplier[280:310] = 1.5  # Another volatile period
volatility_multiplier[400:430] = 2.0  # Major volatility

adjusted_returns = daily_returns * volatility_multiplier + trend
price = initial_price * np.cumprod(1 + adjusted_returns)

df = pd.DataFrame({"date": dates, "price": price})

# Plot - Stock area chart
plot = (
    ggplot(df, aes(x="date", y="price"))
    + geom_area(fill="#306998", alpha=0.35)
    + geom_line(color="#306998", size=1.2)
    + scale_x_datetime(date_labels="%b %Y", date_breaks="3 months")
    + scale_y_continuous(labels=lambda x: [f"${v:.0f}" for v in x])
    + labs(x="Date", y="Stock Price (USD)", title="area-stock-range · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(angle=45, ha="right"),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", size=0.4, alpha=0.3),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
