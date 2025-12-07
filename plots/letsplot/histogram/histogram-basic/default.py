"""
histogram-basic: Basic Histogram
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import LetsPlot, aes, element_text, geom_histogram, ggplot, ggsave, ggsize, labs, theme, theme_minimal


LetsPlot.setup_html()

# Data
np.random.seed(42)
data = pd.DataFrame({"value": np.random.normal(100, 15, 500)})

# Plot
plot = (
    ggplot(data, aes(x="value"))
    + geom_histogram(bins=30, fill="#306998", color="white", alpha=0.8)
    + labs(x="Value", y="Frequency", title="Basic Histogram")
    + theme_minimal()
    + theme(plot_title=element_text(size=20), axis_title=element_text(size=20), axis_text=element_text(size=16))
    + ggsize(1600, 900)
)

# Save - scale 3x to get 4800 x 2700 px
ggsave(plot, "plot.png", path=".", scale=3)
