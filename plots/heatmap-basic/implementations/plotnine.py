""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 89/100 | Updated: 2026-02-15
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_rect,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    labs,
    scale_color_identity,
    scale_fill_gradient2,
    scale_x_discrete,
    scale_y_discrete,
    theme,
    theme_minimal,
)


# Data - 8x8 matrix: quarterly growth rates (%) by department
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "Finance", "Operations", "HR", "Research", "Support"]
quarters = ["Q1 '23", "Q2 '23", "Q3 '23", "Q4 '23", "Q1 '24", "Q2 '24", "Q3 '24", "Q4 '24"]

# Growth rates with a recovery trend and departmental variation
base_trend = np.linspace(-15, 20, 8)
dept_offsets = np.array([-5, 8, 12, -2, 3, -8, 6, -4])
values = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        values[i, j] = round(base_trend[j] + dept_offsets[i] + np.random.normal(0, 4), 1)

# Long-form DataFrame
records = []
for i, dept in enumerate(departments):
    for j, qtr in enumerate(quarters):
        records.append({"Department": dept, "Quarter": qtr, "Growth": values[i, j]})

df = pd.DataFrame(records)
df["Quarter"] = pd.Categorical(df["Quarter"], categories=quarters, ordered=True)
df["Department"] = pd.Categorical(df["Department"], categories=departments[::-1], ordered=True)

# Conditional text color: white on dark blue cells, dark on light cells
df["text_color"] = df["Growth"].apply(lambda v: "white" if v < -10 else "#333333")

# Format labels with sign
df["label"] = df["Growth"].apply(lambda v: f"{v:+.1f}")

# Plot
plot = (
    ggplot(df, aes(x="Quarter", y="Department"))
    + geom_tile(aes(fill="Growth"), color="white", size=0.8)
    + geom_text(aes(label="label", color="text_color"), size=11, fontweight="bold", show_legend=False)
    + scale_fill_gradient2(low="#306998", mid="#f5f5f0", high="#FFD43B", midpoint=0, name="Growth (%)")
    + scale_color_identity()
    + scale_x_discrete(expand=(0, 0.5))
    + scale_y_discrete(expand=(0, 0.5))
    + labs(x="Quarter", y="Department", title="Quarterly Growth by Department · heatmap-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(family="sans-serif"),
        plot_title=element_text(size=24, ha="center", weight="bold", margin={"b": 15}),
        axis_title_x=element_text(size=20, margin={"t": 10}),
        axis_title_y=element_text(size=20, margin={"r": 10}),
        axis_text_x=element_text(size=16, rotation=45, ha="right", margin={"t": 5}),
        axis_text_y=element_text(size=16, ha="right", margin={"r": 5}),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
