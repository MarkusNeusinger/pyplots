"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-24
"""

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

# Create raincloud plot: half-violin (cloud) + box plot + jittered points (rain)
plot = (
    ggplot(df, aes(x="condition", y="reaction_time", fill="condition"))
    # Half-violin (cloud) - show only right half
    + geom_violin(trim=False, show_half=1, show_legend=False, size=0.8, alpha=0.7)
    # Box plot - positioned in center
    + geom_boxplot(
        width=0.12, outlier_shape=None, fill="white", color="#333333", size=0.8, alpha=0.95, show_legend=False
    )
    # Jittered points (rain) - spread for visibility
    + geom_jitter(width=0.08, height=0, size=2.5, alpha=0.5, color="#1a1a1a", show_legend=False)
    + scale_fill_manual(values=["#306998", "#FFD43B", "#5BA85B"])
    + labs(x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
