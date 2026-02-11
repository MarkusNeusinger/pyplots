"""pyplots.ai
area-basic: Basic Area Chart
Library: plotnine 0.15.3 | Python 3.14.2
Quality: /100 | Updated: 2026-02-11
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_text,
    geom_area,
    geom_line,
    geom_smooth,
    ggplot,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
base_traffic = 5000
trend = np.linspace(0, 2000, 30)
weekly_pattern = 1000 * np.sin(np.arange(30) * 2 * np.pi / 7)
# Increasing amplitude over time for better feature coverage
amplitude_growth = np.linspace(1.0, 1.8, 30)
noise = np.random.normal(0, 500, 30) * amplitude_growth
visitors = base_traffic + trend + weekly_pattern * amplitude_growth + noise
visitors = np.maximum(visitors, 1000)

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Plot
plot = (
    ggplot(df, aes(x="date", y="visitors"))
    + geom_area(fill="#306998", alpha=0.35)
    + geom_line(color="#306998", size=1.5)
    + geom_smooth(method="lowess", color="#FFD43B", size=1.2, se=False, span=0.5)
    + annotate(
        "text",
        x=dates[df["visitors"].idxmax()],
        y=df["visitors"].max() + 300,
        label="Peak",
        size=14,
        color="#306998",
        fontweight="bold",
    )
    + labs(x="Date (January 2024)", y="Daily Visitors (count)", title="area-basic · plotnine · pyplots.ai")
    + scale_x_datetime(date_labels="%b %d")
    + scale_y_continuous(labels=lambda lst: [f"{int(v):,}" for v in lst])
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
