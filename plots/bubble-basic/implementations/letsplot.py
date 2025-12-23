"""pyplots.ai
bubble-basic: Basic Bubble Chart
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
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
    + geom_point(color="#306998", alpha=0.6)
    + scale_size(range=[3, 18], name="Market Share (%)")
    + labs(x="Revenue (Million USD)", y="Growth Rate (%)", title="bubble-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
plot.to_html("plot.html")
