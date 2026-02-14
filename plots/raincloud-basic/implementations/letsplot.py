""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: letsplot 4.8.2 | Python 3.14
Quality: 79/100 | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from lets_plot import *
from lets_plot.export import ggsave


LetsPlot.setup_html()

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

# Create raincloud plot: half-violin (cloud) + box plot + jittered points (rain)
# HORIZONTAL orientation: x=values, y=categories
# Layout: cloud ABOVE (positive y), boxplot on baseline, rain BELOW (negative y)
plot = (
    ggplot(df, aes(x="reaction_time", y="condition", fill="condition", color="condition"))
    # Half-violin (cloud) - nudged upward (positive y direction = above category)
    + geom_violin(
        trim=False,
        show_half=1,
        size=0.8,
        alpha=0.7,
        position=position_nudge(y=0.15),
        tooltips=layer_tooltips()
        .title("@condition")
        .line("Distribution of reaction times")
        .format("@..density..", ".3f"),
    )
    # Box plot - centered on category baseline
    + geom_boxplot(
        width=0.1,
        outlier_shape=None,
        fill="white",
        color="#333333",
        size=0.8,
        alpha=0.95,
        show_legend=False,
        tooltips=layer_tooltips()
        .title("Summary Statistics")
        .line("Median: @..middle..")
        .line("Q1: @..lower..")
        .line("Q3: @..upper.."),
    )
    # Jittered points (rain) - positioned BELOW (negative y = downward from category)
    # Using condition colors for visual cohesion
    + geom_jitter(
        width=0,
        height=0.06,
        size=2.5,
        alpha=0.6,
        shape=21,
        stroke=0.3,
        show_legend=False,
        position=position_nudge(y=-0.2),
        tooltips=layer_tooltips().line("Reaction Time|@reaction_time ms"),
    )
    # Colors
    + scale_fill_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    + scale_color_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    # Labels and title
    + labs(
        x="Reaction Time (ms)", y="Experimental Condition", title="raincloud-basic \u00b7 letsplot \u00b7 pyplots.ai"
    )
    # Theme
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        legend_title=element_blank(),
        legend_text=element_text(size=14),
        legend_position=[0.92, 0.92],
        legend_justification=[1, 1],
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="rgba(0, 0, 0, 0.15)", size=0.5),
    )
    + ggsize(1600, 900)
    # Lets-plot distinctive feature: coordinated color flavor for cohesive styling
    + flavor_high_contrast_light()
)

# Save outputs - using simple filenames as required
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
