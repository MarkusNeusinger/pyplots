"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_flip,
    element_blank,
    element_text,
    geom_boxplot,
    geom_point,
    geom_violin,
    ggplot,
    labs,
    position_nudge,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
)


# Data - Reaction times (ms) for psychology experiment
np.random.seed(42)

# Control group: Normal distribution centered at 450ms
control = np.random.normal(450, 60, 80)

# Treatment A: Faster responses, centered at 380ms
treatment_a = np.random.normal(380, 50, 80)

# Treatment B: Bimodal distribution to show distribution shape advantage
treatment_b = np.concatenate([np.random.normal(350, 30, 50), np.random.normal(480, 35, 30)])

df = pd.DataFrame(
    {
        "group": ["Control"] * 80 + ["Treatment A"] * 80 + ["Treatment B"] * 80,
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Create numeric x for positioning (used for jittered points offset)
group_mapping = {"Control": 1, "Treatment A": 2, "Treatment B": 3}
df["group_num"] = df["group"].map(group_mapping)
# Offset for rain points
df["group_rain"] = df["group_num"] - 0.25

# Add jitter to rain positions
np.random.seed(42)
df["jitter"] = np.random.uniform(-0.08, 0.08, len(df))
df["group_rain_jitter"] = df["group_rain"] + df["jitter"]

# Python colors
colors = ["#306998", "#FFD43B", "#4B8BBE"]

# Create raincloud plot with horizontal orientation for readability
plot = (
    ggplot(df, aes(x="group", y="reaction_time", fill="group", color="group"))
    # Half-violin (cloud) - positioned to one side
    + geom_violin(style="left", alpha=0.7, size=0.8, position=position_nudge(x=0.15))
    # Box plot in the middle - thin and minimal
    + geom_boxplot(width=0.12, alpha=0.9, outlier_shape="", size=0.8)
    # Jittered points (rain) - using pre-calculated positions
    + geom_point(aes(x="group_rain_jitter"), alpha=0.5, size=2)
    + coord_flip()
    + scale_fill_manual(values=colors)
    + scale_color_manual(values=colors)
    + labs(x="Experimental Group", y="Reaction Time (ms)", title="raincloud-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
        panel_grid_minor=element_blank(),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
