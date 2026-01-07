""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-07
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_line,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Monthly product sales over 2 years (small multiples for progressive reveal)
np.random.seed(42)

n_months = 24
month_numbers = np.arange(1, n_months + 1)

# Generate realistic sales data with seasonal pattern and growth trend
base_sales = 50000
trend = np.linspace(0, 20000, n_months)
seasonal = 8000 * np.sin(2 * np.pi * month_numbers / 12 - np.pi / 2)
noise = np.random.normal(0, 3000, n_months)
sales = base_sales + trend + seasonal + noise

# Create stages for small multiples (showing progression at key points)
stages = [6, 12, 18, 24]
stage_labels = ["6 Months", "12 Months", "18 Months", "24 Months (Complete)"]

# Build main dataframe for faceted plot (all points)
data_list = []
for stage, label in zip(stages, stage_labels, strict=True):
    stage_df = pd.DataFrame({"month": month_numbers[:stage], "sales": sales[:stage], "stage": label})
    data_list.append(stage_df)

df = pd.concat(data_list, ignore_index=True)
df["stage"] = pd.Categorical(df["stage"], categories=stage_labels, ordered=True)

# Separate dataframe for current (highlighted) points only
current_data = []
for stage, label in zip(stages, stage_labels, strict=True):
    current_data.append({"month": month_numbers[stage - 1], "sales": sales[stage - 1], "stage": label})

df_current = pd.DataFrame(current_data)
df_current["stage"] = pd.Categorical(df_current["stage"], categories=stage_labels, ordered=True)

# Add point_type column for legend
df["point_type"] = "Historical"
df_current["point_type"] = "Current"

# Create the small multiples plot showing progressive line building
plot = (
    ggplot(df, aes(x="month", y="sales"))
    + geom_line(color="#306998", size=1.5, alpha=0.9)
    + geom_point(aes(color="point_type"), size=3, alpha=0.8)
    + geom_point(data=df_current, mapping=aes(x="month", y="sales", color="point_type"), size=5, stroke=1.5)
    + facet_wrap("~stage", ncol=2)
    + scale_x_continuous(breaks=[1, 6, 12, 18, 24], labels=["Jan '23", "Jun '23", "Jan '24", "Jun '24", "Dec '24"])
    + scale_y_continuous(labels=lambda x: [f"${v / 1000:.0f}K" for v in x])
    + scale_color_manual(values={"Historical": "#306998", "Current": "#FFD43B"}, name="Data Point")
    + labs(
        title="line-animated-progressive · plotnine · pyplots.ai",
        subtitle="Progressive Line Reveal: Monthly Sales Growth Over Time",
        x="Time Period",
        y="Monthly Sales (USD)",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=22, weight="bold", ha="center"),
        plot_subtitle=element_text(size=16, ha="center", color="#666666"),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        axis_text_x=element_text(rotation=45, ha="right"),
        strip_text=element_text(size=16, weight="bold"),
        strip_background=element_rect(fill="#f0f0f0", color=None),
        panel_spacing=0.15,
        plot_background=element_rect(fill="white", color=None),
        panel_background=element_rect(fill="white", color=None),
        panel_grid_major=element_line(color="#cccccc", alpha=0.3),
        panel_grid_minor=element_line(color="#e0e0e0", alpha=0.2),
        legend_position="bottom",
        legend_title=element_text(size=14, weight="bold"),
        legend_text=element_text(size=12),
    )
)

# Save
plot.save("plot.png", dpi=300)
