"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-07
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
    scale_color_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Monthly website traffic over 2 years
np.random.seed(42)
n_points = 24
months = np.arange(1, n_points + 1)

# Traffic with seasonal pattern and growth trend
base_traffic = 50000
trend = np.linspace(0, 30000, n_points)
seasonal = 8000 * np.sin(2 * np.pi * months / 12)
noise = np.random.normal(0, 3000, n_points)
traffic = base_traffic + trend + seasonal + noise

# Create small multiples showing progressive stages
stages = [6, 12, 18, 24]
stage_labels = ["1. Q2 2023", "2. Q4 2023", "3. Q2 2024", "4. Complete"]

dfs = []
for stage, label in zip(stages, stage_labels, strict=True):
    stage_df = pd.DataFrame(
        {
            "month": months[:stage],
            "traffic": traffic[:stage],
            "stage": label,
            "is_latest": [False] * (stage - 1) + [True],
        }
    )
    dfs.append(stage_df)

df = pd.concat(dfs, ignore_index=True)

# Create plot with small multiples
plot = (
    ggplot(df, aes(x="month", y="traffic"))
    + geom_line(color="#306998", size=2, alpha=0.9)
    + geom_point(aes(color="is_latest"), size=4, alpha=0.8)
    + scale_color_manual(values={"True": "#FFD43B", "False": "#306998"}, guide="none")
    + facet_wrap("stage", ncol=2)
    + scale_x_continuous(breaks=[6, 12, 18, 24], labels=["Jun '23", "Dec '23", "Jun '24", "Dec '24"])
    + labs(title="line-animated-progressive \u00b7 letsplot \u00b7 pyplots.ai", x="Time Period", y="Monthly Visitors")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=26),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        strip_text=element_text(size=18),
        legend_text=element_text(size=16),
        panel_grid=element_line(color="#CCCCCC", size=0.4, linetype="dashed"),
        panel_background=element_rect(fill="#FAFAFA"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
