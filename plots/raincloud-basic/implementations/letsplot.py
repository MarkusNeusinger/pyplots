""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-25
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
# Layout: cloud on right, boxplot slightly left of center, rain on left (like rain falling from cloud)
plot = (
    ggplot(df, aes(x="condition", y="reaction_time", fill="condition", color="condition"))
    # Half-violin (cloud) - nudged to right side
    + geom_violin(
        trim=False,
        show_half=1,  # Show only right/upper half (the "cloud")
        size=0.8,
        alpha=0.7,
        position=position_nudge(x=0.15),
        tooltips=layer_tooltips()
        .title("@condition")
        .line("Distribution of reaction times")
        .format("@..density..", ".3f"),
    )
    # Box plot - slightly left of center
    + geom_boxplot(
        width=0.1,
        outlier_shape=None,
        fill="white",
        color="#333333",
        size=0.8,
        alpha=0.95,
        show_legend=False,
        position=position_nudge(x=-0.02),
        tooltips=layer_tooltips()
        .title("Summary Statistics")
        .line("Median: @..middle..")
        .line("Q1: @..lower..")
        .line("Q3: @..upper.."),
    )
    # Jittered points (rain) - clearly positioned to left of boxplot (rain falling from cloud)
    + geom_jitter(
        width=0.04,
        height=0,
        size=2.5,
        alpha=0.6,
        shape=21,  # Filled circle with border
        fill="#1a1a1a",
        color="#1a1a1a",
        show_legend=False,
        position=position_nudge(x=-0.2),
        tooltips=layer_tooltips().line("Reaction Time|@reaction_time ms"),
    )
    # Colors
    + scale_fill_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    + scale_color_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    # Labels and title
    + labs(x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic · letsplot · pyplots.ai")
    # Legend positioned at bottom-right to not cover data
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        legend_title=element_blank(),
        legend_text=element_text(size=14),
        legend_position=[0.92, 0.15],
        legend_justification=[1, 0],
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="rgba(0, 0, 0, 0.15)", size=0.5),
    )
    + ggsize(1600, 900)
    # Lets-plot distinctive feature: coordinated color flavor for cohesive styling
    + flavor_high_contrast_light()
)

# Save outputs - using simple filenames as required
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
