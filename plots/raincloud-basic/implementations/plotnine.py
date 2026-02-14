"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotnine 0.15.3 | Python 3.14
Quality: /100 | Updated: 2026-02-14
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
    geom_jitter,
    geom_violin,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    stage,
    theme,
    theme_minimal,
)


# Data - Reaction times (ms) for three experimental conditions
np.random.seed(42)

control = np.random.normal(450, 60, 80)
treatment_a = np.random.normal(380, 50, 80)
treatment_b = np.concatenate([np.random.normal(350, 40, 50), np.random.normal(500, 45, 30)])

df = pd.DataFrame(
    {
        "condition": (
            ["Control"] * len(control) + ["Treatment A"] * len(treatment_a) + ["Treatment B"] * len(treatment_b)
        ),
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)
df["condition"] = pd.Categorical(df["condition"], categories=["Treatment B", "Treatment A", "Control"], ordered=True)

# Colors
colors = {"Control": "#306998", "Treatment A": "#FFD43B", "Treatment B": "#5BA85B"}

# Cloud shift (positive = right on pre-flip x-axis = upward after coord_flip)
cloud_shift = 0.12

# Plot - horizontal raincloud via coord_flip
# Before flip: x=condition (categorical), y=reaction_time (numeric)
# After flip: categories on y-axis, values on x-axis
plot = (
    ggplot(df, aes(x="condition", y="reaction_time", fill="condition", color="condition"))
    # Cloud (half-violin) - style="right" extends in positive x-direction = upward after flip
    + geom_violin(
        aes(x=stage("condition", after_scale="x+{0}".format(cloud_shift))),
        style="right",
        trim=True,
        scale="width",
        size=0.4,
        alpha=0.85,
        show_legend=False,
    )
    # Boxplot - centered on category baseline
    + geom_boxplot(width=0.08, outlier_shape="", fill="white", color="#333333", size=0.6, alpha=0.95, show_legend=False)
    # Rain (jittered points) - nudged in negative x-direction = downward after flip
    + geom_jitter(
        aes(x=stage("condition", after_scale="x-0.18")), width=0.06, height=0, size=1.8, alpha=0.6, show_legend=False
    )
    + scale_fill_manual(values=colors)
    + scale_color_manual(values=colors)
    + coord_flip()
    + labs(
        x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic \u00b7 plotnine \u00b7 pyplots.ai"
    )
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
