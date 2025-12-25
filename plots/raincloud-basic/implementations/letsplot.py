"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-25
"""

from pathlib import Path

import numpy as np
import pandas as pd
from lets_plot import *


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

# Create raincloud plot: half-violin (cloud) on top + box plot + jittered points (rain) below
# Using horizontal orientation: cloud on right side, boxplot center, rain on left
plot = (
    ggplot(df, aes(x="condition", y="reaction_time", fill="condition", color="condition"))
    # Half-violin (cloud) - show only right half (positive side)
    + geom_violin(
        trim=False,
        show_half=1,  # Show only right/upper half (the "cloud")
        size=0.8,
        alpha=0.7,
        tooltips=layer_tooltips()
        .title("@condition")
        .line("Distribution of reaction times")
        .format("@..density..", ".3f"),
    )
    # Box plot - centered, shows quartiles and median
    + geom_boxplot(
        width=0.12,
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
    # Jittered points (rain) - spread for visibility, positioned to left of center
    + geom_jitter(
        width=0.08,
        height=0,
        size=2.5,
        alpha=0.5,
        shape=21,  # Filled circle with border
        fill="#1a1a1a",
        color="#1a1a1a",
        show_legend=False,
        tooltips=layer_tooltips().line("Reaction Time|@reaction_time ms"),
    )
    # Colors
    + scale_fill_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    + scale_color_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    # Labels and title
    + labs(
        x="Experimental Condition",
        y="Reaction Time (ms)",
        title="raincloud-basic · letsplot · pyplots.ai",
        fill="Condition",
    )
    # Legend positioning - show legend for fill
    + guides(color="none")  # Hide color legend since it duplicates fill
    # Theme
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save outputs
output_dir = Path(__file__).parent
ggsave(plot, str(output_dir / "plot.png"), scale=3)
ggsave(plot, str(output_dir / "plot.html"))
