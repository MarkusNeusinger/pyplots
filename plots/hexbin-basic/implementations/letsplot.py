""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
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
n_points = 5000

# Create multiple clusters to show density patterns
cluster1_x = np.random.randn(n_points // 2) * 1.5 + 2
cluster1_y = np.random.randn(n_points // 2) * 1.5 + 2
cluster2_x = np.random.randn(n_points // 3) * 1.0 - 2
cluster2_y = np.random.randn(n_points // 3) * 1.0 + 1
cluster3_x = np.random.randn(n_points // 6) * 0.8 + 0
cluster3_y = np.random.randn(n_points // 6) * 0.8 - 2

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

df = pd.DataFrame({"x": x, "y": y})

# Plot - Hexagonal binning to show density patterns
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_hex(bins=[30, 30])
    + scale_fill_viridis(name="Count", option="viridis")
    + labs(x="X Coordinate", y="Y Coordinate", title="hexbin-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
        panel_grid=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
