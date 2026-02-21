""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: letsplot 4.8.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
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
    layer_tooltips,
    scale_fill_viridis,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Simulated GPS ping density across a metro area (km from city center)
np.random.seed(42)
n_points = 10000

# Downtown core - dense commercial district
downtown_east = np.random.randn(n_points // 2) * 1.5 + 4
downtown_north = np.random.randn(n_points // 2) * 1.5 + 3

# University campus - moderate foot traffic
campus_east = np.random.randn(n_points // 3) * 1.0 - 3
campus_north = np.random.randn(n_points // 3) * 1.0 + 1

# Transit hub - tight cluster of commuters
transit_east = np.random.randn(n_points // 6) * 0.5 + 0.5
transit_north = np.random.randn(n_points // 6) * 0.5 - 3.5

east_km = np.concatenate([downtown_east, campus_east, transit_east])
north_km = np.concatenate([downtown_north, campus_north, transit_north])

df = pd.DataFrame({"east_km": east_km, "north_km": north_km})

# Plot - Hexagonal binning to reveal pedestrian density hotspots
plot = (
    ggplot(df, aes(x="east_km", y="north_km"))
    + geom_hex(
        aes(fill="..count.."),
        bins=[30, 30],
        color="#FFFFFF",
        size=0.3,
        tooltips=layer_tooltips()
        .title("Hex Bin")
        .line("pings|@..count..")
        .line("density|@..density..")
        .format("@..density..", ".3f"),
    )
    + scale_fill_viridis(name="Ping Count", option="viridis")
    + labs(
        x="East-West (km from center)",
        y="North-South (km from center)",
        title="hexbin-basic \u00b7 letsplot \u00b7 pyplots.ai",
    )
    + theme_minimal()
    + theme(
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        plot_title=element_text(size=26),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        panel_grid=element_line(color="#E0E0E0", size=0.3, linetype="dashed"),
        panel_background=element_rect(fill="#FAFAFA"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive tooltips
ggsave(plot, "plot.html", path=".")
