"""pyplots.ai
scatter-marginal: Scatter Plot with Marginal Distributions
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-26
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - bivariate data with correlation
np.random.seed(42)
n = 200
x = np.random.randn(n) * 2 + 10
y = x * 0.8 + np.random.randn(n) * 1.5 + 2

df = pd.DataFrame({"x": x, "y": y})

# Calculate axis limits for aligned marginal plots
x_min, x_max = df["x"].min() - 0.5, df["x"].max() + 0.5
y_min, y_max = df["y"].min() - 0.5, df["y"].max() + 0.5

# Main scatter plot
main_scatter = (
    ggplot(df, aes(x="x", y="y"))  # noqa: F405
    + geom_point(color="#306998", size=4, alpha=0.65)  # noqa: F405
    + labs(x="X Value", y="Y Value")  # noqa: F405
    + scale_x_continuous(limits=[x_min, x_max])  # noqa: F405
    + scale_y_continuous(limits=[y_min, y_max])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
    )
)

# Top marginal histogram
top_hist = (
    ggplot(df, aes(x="x"))  # noqa: F405
    + geom_histogram(fill="#306998", color="white", alpha=0.7, bins=25)  # noqa: F405
    + scale_x_continuous(limits=[x_min, x_max])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_blank(),  # noqa: F405
        axis_text_x=element_blank(),  # noqa: F405
        axis_ticks_x=element_blank(),  # noqa: F405
        axis_text_y=element_text(size=14),  # noqa: F405
    )
)

# Right marginal histogram
right_hist = (
    ggplot(df, aes(x="y"))  # noqa: F405
    + geom_histogram(fill="#306998", color="white", alpha=0.7, bins=25)  # noqa: F405
    + coord_flip()  # noqa: F405
    + scale_x_continuous(limits=[y_min, y_max])  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_blank(),  # noqa: F405
        axis_text_y=element_blank(),  # noqa: F405
        axis_ticks_y=element_blank(),  # noqa: F405
        axis_text_x=element_text(size=14),  # noqa: F405
    )
)

# Title plot (text-only)
title_plot = (
    ggplot()  # noqa: F405
    + geom_blank()  # noqa: F405
    + ggtitle("scatter-marginal · letsplot · pyplots.ai")  # noqa: F405
    + theme_void()  # noqa: F405
    + theme(plot_title=element_text(size=24, hjust=0.5))  # noqa: F405
)

# Combine using ggbunch (new API)
# Regions: (x, y, width, height) - relative coordinates
combined = (
    ggbunch(  # noqa: F405
        [title_plot, top_hist, main_scatter, right_hist],
        [
            (0, 0, 1.0, 0.08),  # Title at top
            (0, 0.08, 0.8, 0.2),  # Top histogram
            (0, 0.28, 0.8, 0.72),  # Main scatter plot
            (0.8, 0.28, 0.2, 0.72),  # Right histogram
        ],
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save as PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(combined, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(combined, filename="plot.html", path=".")
