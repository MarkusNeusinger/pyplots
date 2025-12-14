"""
bubble-basic: Basic Bubble Chart
Library: letsplot
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

# Data
np.random.seed(42)
n = 50

x = np.random.randn(n) * 15 + 50
y = x * 0.6 + np.random.randn(n) * 10 + 20
size_values = np.abs(np.random.randn(n) * 30 + 50)

df = pd.DataFrame({"x": x, "y": y, "size": size_values})

# Plot
plot = (
    ggplot(df, aes(x="x", y="y", size="size"))
    + geom_point(color="#306998", alpha=0.6)
    + scale_size(range=[3, 20], name="Size Value")
    + labs(x="X Value", y="Y Value", title="bubble-basic · letsplot · pyplots.ai")
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
