""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 86/100 | Updated: 2026-02-15
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
# Include a wider range with a few extreme outliers for feature coverage
base_trend = np.linspace(-18, 22, 8)
dept_offsets = np.array([-6, 10, 14, -3, 4, -10, 8, -5])
values = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        values[i, j] = round(base_trend[j] + dept_offsets[i] + np.random.normal(0, 4), 1)

# Inject a few distinctive extreme values for storytelling
values[5, 0] = -32.5  # HR deep crisis in Q1 '23
values[2, 7] = 38.2  # Sales strong recovery in Q4 '24
values[6, 6] = 33.7  # Research surge in Q3 '24

# Long-form DataFrame
records = []
for i, dept in enumerate(departments):
    for j, qtr in enumerate(quarters):
        records.append({"Department": dept, "Quarter": qtr, "Growth (%)": values[i, j]})

df = pd.DataFrame(records)
df["Quarter"] = pd.Categorical(df["Quarter"], categories=quarters, ordered=True)
df["Department"] = pd.Categorical(df["Department"], categories=departments[::-1], ordered=True)

# Conditional text color for optimal contrast on all cell backgrounds
df["text_color"] = df["Growth (%)"].apply(lambda v: "white" if v < -12 else ("#444444" if v < 18 else "#5a3e00"))

# Format labels with sign
df["label"] = df["Growth (%)"].apply(lambda v: f"{v:+.1f}")

# Plot
plot = (
    ggplot(df, aes(x="Quarter", y="Department"))
    + geom_tile(aes(fill="Growth (%)"), color="white", size=1.0)
    + geom_text(aes(label="label", color="text_color"), size=10, fontweight="bold", show_legend=False)
    + scale_fill_gradient2(
        low="#1a4971", mid="#f0eeeb", high="#cc8400", midpoint=0, name="Growth (%)", limits=(-35, 40)
    )
    + scale_color_identity()
    + scale_x_discrete(expand=(0, 0.5))
    + scale_y_discrete(expand=(0, 0.5))
    + labs(
        x="Quarter",
        y="Department",
        title="Quarterly Growth by Department · heatmap-basic · plotnine · pyplots.ai",
        subtitle="Year-over-year growth rate (%) across departments, Q1 2023 – Q4 2024",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(family="sans-serif"),
        plot_title=element_text(size=22, ha="center", weight="bold", margin={"b": 4}),
        plot_subtitle=element_text(size=15, ha="center", color="#666666", margin={"b": 12}),
        axis_title_x=element_text(size=18, margin={"t": 10}),
        axis_title_y=element_text(size=18, margin={"r": 8}),
        axis_text_x=element_text(size=15, rotation=45, ha="right", margin={"t": 5}),
        axis_text_y=element_text(size=15, ha="right", margin={"r": 5}),
        legend_title=element_text(size=15, weight="bold"),
        legend_text=element_text(size=13),
        legend_position="right",
        legend_key_height=40,
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white", color="none"),
        plot_background=element_rect(fill="#fafafa", color="none"),
        plot_margin=0.02,
    )
)

plot.save("plot.png", dpi=300, verbose=False)
