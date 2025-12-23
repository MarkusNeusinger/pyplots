"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-23
"""
# ruff: noqa: F405

import os
import shutil

import pandas as pd
from lets_plot import *  # noqa: F403, F405


LetsPlot.setup_html()

# Data - Multiple KPIs for a dashboard view
metrics = ["Revenue", "Profit", "Customer Satisfaction", "Market Share"]
actual = [275, 82, 4.2, 35]
target = [300, 90, 4.5, 40]
poor = [100, 40, 2.5, 15]
satisfactory = [200, 70, 3.5, 30]
good = [350, 100, 5.0, 50]

n_metrics = len(metrics)

# Normalize all values to percentage of maximum
actual_pct = [actual[i] / good[i] * 100 for i in range(n_metrics)]
target_pct = [target[i] / good[i] * 100 for i in range(n_metrics)]
poor_pct = [poor[i] / good[i] * 100 for i in range(n_metrics)]
satisfactory_pct = [satisfactory[i] / good[i] * 100 for i in range(n_metrics)]

# Create long-form dataframe for stacked ranges
# Each row represents the width of one range segment
range_data = []
for i in range(n_metrics):
    range_data.append({"metric": metrics[i], "range_type": "1_Poor", "width": poor_pct[i]})
    range_data.append(
        {"metric": metrics[i], "range_type": "2_Satisfactory", "width": satisfactory_pct[i] - poor_pct[i]}
    )
    range_data.append({"metric": metrics[i], "range_type": "3_Good", "width": 100 - satisfactory_pct[i]})

range_df = pd.DataFrame(range_data)

# Actual values dataframe
actual_df = pd.DataFrame({"metric": metrics, "actual": actual_pct})

# Target dataframe
target_df = pd.DataFrame({"metric": metrics, "target": target_pct})

# Create the plot using horizontal stacked bar for ranges
plot = (
    ggplot()
    # Stacked bar for qualitative ranges (full width background)
    + geom_bar(
        data=range_df,
        mapping=aes(x="width", y="metric", fill="range_type"),
        stat="identity",
        orientation="y",
        position="stack",
        width=0.7,
    )
    # Actual value bar (narrower overlay)
    + geom_bar(
        data=actual_df,
        mapping=aes(x="actual", y="metric"),
        stat="identity",
        orientation="y",
        fill="#306998",
        color="#1e4461",
        width=0.4,
        size=0.5,
    )
    # Target marker as thin vertical line using geom_tile
    + geom_tile(data=target_df, mapping=aes(x="target", y="metric"), fill="black", width=0.6, height=0.55)
    # Grayscale fills for ranges
    + scale_fill_manual(
        values=["#555555", "#999999", "#CCCCCC"], name="Performance Range", labels=["Poor", "Satisfactory", "Good"]
    )
    # Axis labels
    + scale_x_continuous(name="Performance (%)", limits=[0, 110])
    + scale_y_discrete(limits=list(reversed(metrics)))
    + labs(title="bullet-basic · letsplot · pyplots.ai", y="")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title_x=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=18),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="bottom",
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(size=0.5, color="#E0E0E0"),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scaled 3x for 4800x2700)
ggsave(plot, "plot.png", scale=3)

# Save as HTML for interactive viewing
ggsave(plot, "plot.html")

# Move files from lets-plot-images subfolder to current directory
if os.path.exists("lets-plot-images/plot.png"):
    shutil.move("lets-plot-images/plot.png", "plot.png")
if os.path.exists("lets-plot-images/plot.html"):
    shutil.move("lets-plot-images/plot.html", "plot.html")
if os.path.exists("lets-plot-images"):
    shutil.rmtree("lets-plot-images")
