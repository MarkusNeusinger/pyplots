"""pyplots.ai
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
    element_rect,
    element_text,
    geom_histogram,
    geom_text,
    geom_vline,
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
female_heights = np.random.normal(165, 7, 300)
male_heights = np.random.normal(178, 8, 300)
heights = np.concatenate([female_heights, male_heights])
df = pd.DataFrame({"heights": heights})

# Compute population means for annotation
female_mean = float(np.mean(female_heights))
male_mean = float(np.mean(male_heights))

# Annotation data for mean labels
annotations = pd.DataFrame(
    {
        "x": [female_mean, male_mean],
        "y": [62, 62],
        "label": [f"Women avg\n{female_mean:.1f} cm", f"Men avg\n{male_mean:.1f} cm"],
    }
)

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
    # Mean reference lines for each population
    + geom_vline(xintercept=female_mean, color="#E07B39", size=1.2, linetype="dashed", alpha=0.9)
    + geom_vline(xintercept=male_mean, color="#E07B39", size=1.2, linetype="dashed", alpha=0.9)
    # Mean labels
    + geom_text(data=annotations, mapping=aes(x="x", y="y", label="label"), size=12, color="#C05E20", fontface="bold")
    + scale_x_continuous(name="Height (cm)", format=".0f", limits=[140, 205])
    + scale_y_continuous(name="Frequency", format="d")
    + labs(
        title="histogram-basic \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle="Bimodal distribution of human heights \u2014 two overlapping populations",
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        plot_subtitle=element_text(size=16, color="#666666"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.5),
        plot_background=element_rect(fill="white", color="white"),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
