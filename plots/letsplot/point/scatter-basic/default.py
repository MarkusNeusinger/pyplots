"""
scatter-basic: Basic Scatter Plot
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import LetsPlot, aes, element_text, geom_point, ggplot, ggsave, ggsize, labs, theme


LetsPlot.setup_html()

# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

data = pd.DataFrame({"x": x, "y": y})

# Plot
plot = (
    ggplot(data, aes(x="x", y="y"))
    + geom_point(color="#306998", size=4, alpha=0.7)
    + labs(x="X Value", y="Y Value", title="Basic Scatter Plot")
    + ggsize(1600, 900)
    + theme(plot_title=element_text(size=20), axis_title=element_text(size=20), axis_text=element_text(size=16))
)

# Save (scale 3x to get 4800 × 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)
