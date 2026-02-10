""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: letsplot 4.8.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Daily coffee consumption vs productivity score across office workers
np.random.seed(42)
n = 150
coffee_cups = np.random.gamma(shape=2.5, scale=1.2, size=n)
coffee_cups = np.clip(coffee_cups, 0.5, 8.0)
# Productivity peaks around 3-4 cups, then tapers off slightly
productivity = 55 + 12 * coffee_cups - 1.2 * coffee_cups**2 + np.random.randn(n) * 6
productivity = np.clip(productivity, 30, 100)

df = pd.DataFrame({"coffee_cups": np.round(coffee_cups, 1), "productivity": np.round(productivity, 1)})

# Plot
plot = (
    ggplot(df, aes(x="coffee_cups", y="productivity"))  # noqa: F405
    + geom_point(  # noqa: F405
        color="#2A6F97",
        fill="#61A5C2",
        size=7,
        alpha=0.65,
        shape=21,
        stroke=1.2,
        tooltips=layer_tooltips()  # noqa: F405
        .line("Coffee|@coffee_cups cups/day")
        .line("Productivity|@productivity"),
    )
    + labs(  # noqa: F405
        x="Daily Coffee Intake (cups)", y="Productivity Score", title="scatter-basic \u00b7 letsplot \u00b7 pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + scale_x_continuous(breaks=[1, 2, 3, 4, 5, 6, 7, 8])  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16, color="#4A4A4A"),  # noqa: F405
        axis_title=element_text(size=20, color="#2D2D2D"),  # noqa: F405
        plot_title=element_text(size=26, color="#1B1B1B"),  # noqa: F405
        panel_background=element_rect(fill="#FAFBFC"),  # noqa: F405
        plot_background=element_rect(fill="white"),  # noqa: F405
        panel_grid_major=element_line(color="#E0E4E8", size=0.5),  # noqa: F405
        panel_grid_minor=element_line(color="#EEF0F2", size=0.3),  # noqa: F405
        axis_line=element_line(color="#CCCCCC", size=0.8),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
