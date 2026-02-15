""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 80/100 | Updated: 2026-02-15
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    layer_tooltips,
    scale_size,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - market analysis scenario: companies by revenue vs growth with market share
np.random.seed(42)
n = 40

# Revenue (millions USD)
revenue = np.random.uniform(10, 200, n)
# Growth rate (%) - loosely correlated with revenue
growth_rate = 25 - revenue * 0.08 + np.random.randn(n) * 8
# Market share (%) - the bubble size dimension
market_share = np.abs(np.random.randn(n) * 8 + 12)

df = pd.DataFrame({"revenue": revenue, "growth_rate": growth_rate, "market_share": market_share})

# Plot
plot = (
    ggplot(df, aes(x="revenue", y="growth_rate", size="market_share"))
    + geom_point(
        color="#306998",
        alpha=0.6,
        tooltips=layer_tooltips()
        .format("revenue", "${.1f}M")
        .format("growth_rate", "{.1f}%")
        .format("market_share", "{.1f}%")
        .line("Revenue|@revenue")
        .line("Growth|@growth_rate")
        .line("Market Share|@market_share"),
    )
    + scale_size(range=[3, 18], name="Market Share (%)")
    + labs(x="Revenue (Million USD)", y="Growth Rate (%)", title="bubble-basic \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        panel_grid_major=element_line(size=0.5, color="#E0E0E0"),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
plot.to_html("plot.html")
