""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-09
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_line,
    geom_point,
    ggplot,
    ggsize,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Monthly website traffic over 2 years showing growth with seasonality
np.random.seed(42)
n_points = 24
months = np.arange(1, n_points + 1)

# Traffic with seasonal pattern and growth trend
base_traffic = 50000
trend = np.linspace(0, 35000, n_points)
seasonal = 10000 * np.sin(2 * np.pi * months / 12)
noise = np.random.normal(0, 2500, n_points)
traffic = base_traffic + trend + seasonal + noise

# Create small multiples showing progressive reveal stages
stages = [6, 12, 18, 24]
stage_labels = ["1. Q2 2023", "2. Q4 2023", "3. Q2 2024", "4. Q4 2024"]

dfs = []
for stage, label in zip(stages, stage_labels, strict=True):
    stage_df = pd.DataFrame({"month": months[:stage], "traffic": traffic[:stage], "stage": label})
    dfs.append(stage_df)

df = pd.concat(dfs, ignore_index=True)

# Create separate dataframe for highlighting latest points
latest_points = []
for stage, label in zip(stages, stage_labels, strict=True):
    latest_points.append({"month": months[stage - 1], "traffic": traffic[stage - 1], "stage": label})
df_latest = pd.DataFrame(latest_points)

# Create plot with small multiples to show progression
plot = (
    ggplot(df, aes(x="month", y="traffic"))
    + geom_line(color="#306998", size=2.5, alpha=0.9)
    + geom_point(color="#306998", size=4, alpha=0.8)
    + geom_point(data=df_latest, mapping=aes(x="month", y="traffic"), color="#FFD43B", size=8, alpha=1.0)
    + facet_wrap("stage", ncol=2)
    + scale_x_continuous(breaks=[6, 12, 18, 24], labels=["Jun '23", "Dec '23", "Jun '24", "Dec '24"], limits=[0, 25])
    + scale_y_continuous(limits=[30000, 100000])
    + labs(title="line-animated-progressive · letsplot · pyplots.ai", x="Time Period", y="Monthly Visitors")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        strip_text=element_text(size=20, face="bold"),
        panel_grid_major=element_line(color="#DDDDDD", size=0.5),
        panel_grid_minor=element_line(color="#EEEEEE", size=0.3),
        panel_background=element_rect(fill="#FAFAFA"),
        plot_background=element_rect(fill="white"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
