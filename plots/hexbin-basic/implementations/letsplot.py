""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: letsplot unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
    element_rect,
    element_text,
    geom_hex,
    ggplot,
    ggsize,
    labs,
    scale_fill_viridis,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Generate clustered bivariate distribution for density visualization
np.random.seed(42)
n_points = 10000

# Create multiple clusters to demonstrate density patterns in hexbin visualization
cluster1_x = np.random.randn(n_points // 2) * 1.5 + 3
cluster1_y = np.random.randn(n_points // 2) * 1.5 + 3
cluster2_x = np.random.randn(n_points // 3) * 1.2 - 2
cluster2_y = np.random.randn(n_points // 3) * 1.2 + 1
cluster3_x = np.random.randn(n_points // 6) * 0.6 + 0
cluster3_y = np.random.randn(n_points // 6) * 0.6 - 3

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

df = pd.DataFrame({"x": x, "y": y})

# Plot - Hexagonal binning to reveal density patterns
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_hex(bins=[35, 35])
    + scale_fill_viridis(name="Count", option="viridis")
    + labs(x="X Coordinate", y="Y Coordinate", title="hexbin-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        plot_title=element_text(size=26),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        panel_grid=element_line(color="#CCCCCC", size=0.4, linetype="dashed"),
        panel_background=element_rect(fill="#FAFAFA"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
