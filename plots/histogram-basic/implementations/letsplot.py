""" pyplots.ai
histogram-basic: Basic Histogram
Library: letsplot 4.8.2 | Python 3.14.0
Quality: 87/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_histogram,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data
np.random.seed(42)
heights = np.concatenate(
    [
        np.random.normal(165, 7, 300),  # Female heights
        np.random.normal(178, 8, 300),  # Male heights
    ]
)
df = pd.DataFrame({"heights": heights})

# Plot
plot = (
    ggplot(df, aes(x="heights"))
    + geom_histogram(
        bins=30,
        fill="#306998",
        color="white",
        alpha=0.85,
        size=0.5,
        tooltips=layer_tooltips().format("..count..", "d").format("^x", ".1f").line("Count|@..count.."),
    )
    + scale_x_continuous(name="Height (cm)", format=".0f")
    + scale_y_continuous(name="Frequency", format="d")
    + labs(title="histogram-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
