"""
sparkline-basic: Basic Sparkline
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    theme,
)


LetsPlot.setup_html()

# Data - Daily sales figures over 30 days showing realistic trend
np.random.seed(42)
n_points = 30
base_trend = np.linspace(100, 150, n_points)
noise = np.random.randn(n_points) * 8
values = base_trend + noise
values = np.clip(values, 80, 180)

df = pd.DataFrame({"x": range(n_points), "y": values})

# Identify min/max points for highlighting
min_idx = df["y"].idxmin()
max_idx = df["y"].idxmax()
first_idx = 0
last_idx = n_points - 1

highlight_df = df.loc[[min_idx, max_idx, first_idx, last_idx]].copy()
highlight_df["type"] = ["min", "max", "first", "last"]

# Plot - sparkline with minimal chrome
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_line(color="#306998", size=2)
    + geom_point(data=highlight_df[highlight_df["type"] == "min"], color="#DC2626", size=6)
    + geom_point(data=highlight_df[highlight_df["type"] == "max"], color="#16A34A", size=6)
    + geom_point(data=highlight_df[highlight_df["type"].isin(["first", "last"])], color="#306998", size=5)
    + labs(title="sparkline-basic \u00b7 letsplot \u00b7 pyplots.ai")
    + ggsize(1600, 400)  # Wide aspect ratio for sparkline (4:1)
    + theme(
        axis_line=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_title=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_blank(),
        plot_background=element_blank(),
        plot_title=element_text(size=28, hjust=0.5),
    )
)

# Save PNG (scale 3x for 4800x1200 px)
ggsave(plot, "plot.png", scale=3, path=".")

# Save HTML for interactivity
plot.to_html("plot.html")
