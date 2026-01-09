"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-01-09
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403, F405


LetsPlot.setup_html()

# Data: Monthly temperature readings over 5 years
np.random.seed(42)
dates = pd.date_range("2020-01-01", periods=60, freq="ME")
# Simulate temperature with seasonal pattern + trend
months = np.arange(60)
seasonal = 15 * np.sin(2 * np.pi * months / 12)  # Seasonal cycle
trend = 0.02 * months  # Slight warming trend
noise = np.random.normal(0, 2, 60)
temperature = 15 + seasonal + trend + noise  # Base temp ~15°C

df = pd.DataFrame({"date": dates, "month_num": months, "temperature": temperature})

# Create small multiples showing progressive line reveal at key stages
stages = [12, 24, 36, 48, 60]  # Show 1, 2, 3, 4, 5 years
stage_labels = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5 (Complete)"]

# Build data for faceted view with progressive stages
facet_data = []
for i, stage in enumerate(stages):
    stage_df = df.iloc[:stage].copy()
    stage_df["stage"] = stage_labels[i]
    # Mark the most recent point
    stage_df["is_current"] = False
    stage_df.iloc[-1, stage_df.columns.get_loc("is_current")] = True
    facet_data.append(stage_df)

facet_df = pd.concat(facet_data, ignore_index=True)

# Create color gradient to show progression (older = lighter, newer = darker)
facet_df["progress"] = facet_df.groupby("stage").cumcount() / facet_df.groupby("stage")["stage"].transform("count")

# Create the small multiples plot
plot = (
    ggplot(facet_df, aes(x="month_num", y="temperature"))
    + geom_line(aes(color="progress"), size=2, show_legend=False)
    + geom_point(
        data=facet_df[facet_df["is_current"]],
        mapping=aes(x="month_num", y="temperature"),
        color="#FFD43B",
        size=6,
        shape=21,
        fill="#FFD43B",
        stroke=2,
    )
    + scale_color_gradient(low="#a8c7e6", high="#306998")
    + facet_wrap("stage", ncol=5)
    + labs(x="Months Since Jan 2020", y="Temperature (°C)", title="line-animated-progressive · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        strip_text=element_text(size=16, face="bold"),
        panel_grid_major=element_line(color="#cccccc", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG with scale for high resolution
ggsave(plot, "plot.png", path=".", scale=3)

# Also create a single complete view for HTML (interactive)
complete_plot = (
    ggplot(df, aes(x="month_num", y="temperature"))
    + geom_line(color="#306998", size=2)
    + geom_point(aes(color="month_num"), size=4, show_legend=False)
    + scale_color_gradient(low="#a8c7e6", high="#306998", name="Progress")
    + geom_point(
        data=df.iloc[[-1]],
        mapping=aes(x="month_num", y="temperature"),
        color="#FFD43B",
        size=8,
        shape=21,
        fill="#FFD43B",
        stroke=2,
    )
    + labs(x="Months Since Jan 2020", y="Temperature (°C)", title="line-animated-progressive · letsplot · pyplots.ai")
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

# Save interactive HTML
ggsave(complete_plot, "plot.html", path=".")
