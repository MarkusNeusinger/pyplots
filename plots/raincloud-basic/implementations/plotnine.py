"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_flip,
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
    scale_x_continuous,
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

# Build dataframe with numeric x positions
df = pd.DataFrame(
    {
        "condition": ["Control"] * len(control)
        + ["Treatment A"] * len(treatment_a)
        + ["Treatment B"] * len(treatment_b),
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Map conditions to numeric positions (for coord_flip: higher = top)
condition_map = {"Control": 2, "Treatment A": 1, "Treatment B": 0}
df["x_pos"] = df["condition"].map(condition_map).astype(float)

# Add jitter for rain points (below center)
np.random.seed(123)
df["x_rain"] = df["x_pos"] - 0.2 + np.random.uniform(-0.05, 0.05, len(df))

# Colors - dictionary mapping for condition names
colors = {"Control": "#306998", "Treatment A": "#FFD43B", "Treatment B": "#5BA85B"}

# Create raincloud plot with horizontal orientation (coord_flip)
# After flip: Cloud (violin) on TOP, boxplot centered, rain points BELOW
plot = (
    ggplot(df, aes(x="x_pos", y="reaction_time", fill="condition", color="condition"))
    # Half-violin (cloud) - nudged upward (becomes top after flip)
    + geom_violin(position=position_nudge(x=0.2), width=0.45, trim=True, size=0.6, alpha=0.85, show_legend=False)
    # Box plot - centered, narrow, white fill, grouped by condition
    + geom_boxplot(
        aes(group="condition"),
        width=0.1,
        outlier_shape="",
        fill="white",
        color="#333333",
        size=0.6,
        alpha=0.95,
        show_legend=False,
    )
    # Jittered points (rain) - using pre-computed positions below
    + geom_point(aes(x="x_rain"), size=2, alpha=0.6, show_legend=False)
    + scale_fill_manual(values=colors)
    + scale_color_manual(values=colors)
    + scale_x_continuous(breaks=[0, 1, 2], labels=["Treatment B", "Treatment A", "Control"])
    + coord_flip()
    + labs(x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#cccccc", size=0.5),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
