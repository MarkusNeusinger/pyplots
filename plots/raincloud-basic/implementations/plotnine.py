""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_boxplot,
    geom_point,
    geom_violin,
    ggplot,
    labs,
    position_nudge,
    scale_color_manual,
    scale_fill_manual,
    scale_x_discrete,
    theme,
    theme_minimal,
)


# Data - Reaction times (ms) for three experimental conditions
np.random.seed(42)

# Control group: normal distribution centered at 450ms
control = np.random.normal(450, 60, 80)

# Treatment A: faster responses, centered at 380ms
treatment_a = np.random.normal(380, 50, 80)

# Treatment B: bimodal distribution (some fast responders, some slow)
treatment_b = np.concatenate([np.random.normal(350, 40, 50), np.random.normal(500, 45, 30)])

# Build dataframe
df = pd.DataFrame(
    {
        "condition": ["Control"] * len(control)
        + ["Treatment A"] * len(treatment_a)
        + ["Treatment B"] * len(treatment_b),
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Set category order
df["condition"] = pd.Categorical(df["condition"], categories=["Control", "Treatment A", "Treatment B"], ordered=True)

# Create numeric x positions with jitter for rain points
np.random.seed(123)  # Different seed for jitter
condition_map = {"Control": 0, "Treatment A": 1, "Treatment B": 2}
df["x_numeric"] = df["condition"].map(condition_map).astype(float)
# Add jitter and nudge left (-0.2)
df["x_jittered"] = df["x_numeric"] + np.random.uniform(-0.08, 0.08, len(df)) - 0.2

# Colors
colors = ["#306998", "#FFD43B", "#5BA85B"]

# Create raincloud plot
# Layout: violin (cloud) on right side, boxplot centered, jittered points (rain) on left
plot = (
    ggplot(df, aes(x="condition", y="reaction_time", fill="condition"))
    # Half-violin (cloud) - nudged to the right
    + geom_violin(position=position_nudge(x=0.2), width=0.5, trim=True, size=0.8, alpha=0.7, show_legend=False)
    # Box plot - centered, narrow
    + geom_boxplot(
        width=0.12,
        outlier_shape="",  # Hide outliers (shown in scatter)
        fill="white",
        color="#333333",
        size=0.8,
        alpha=0.95,
        show_legend=False,
    )
    # Jittered points (rain) - using pre-computed positions on the left
    + geom_point(aes(x="x_jittered", color="condition"), size=2.5, alpha=0.5, show_legend=False)
    + scale_fill_manual(values=colors)
    + scale_color_manual(values=colors)
    + scale_x_discrete(limits=["Control", "Treatment A", "Treatment B"])
    + labs(x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", size=0.5),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
