""" pyplots.ai
area-basic: Basic Area Chart
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
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
    theme,
    theme_minimal,
)


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
base_traffic = 5000
trend = np.linspace(0, 2000, 30)
weekly_pattern = 1000 * np.sin(np.arange(30) * 2 * np.pi / 7)
noise = np.random.normal(0, 500, 30)
visitors = base_traffic + trend + weekly_pattern + noise
visitors = np.maximum(visitors, 1000)  # Ensure no negative values

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Plot
plot = (
    ggplot(df, aes(x="date", y="visitors"))
    + geom_area(fill="#306998", alpha=0.4)
    + geom_line(color="#306998", size=1.5)
    + labs(x="Date", y="Daily Visitors", title="area-basic · plotnine · pyplots.ai")
    + scale_x_datetime(date_labels="%b %d")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#cccccc", size=0.5, alpha=0.3),
        panel_grid_minor=element_blank(),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
