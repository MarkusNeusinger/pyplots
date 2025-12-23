""" pyplots.ai
histogram-basic: Basic Histogram
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import LetsPlot, aes, element_text, geom_histogram, ggplot, ggsize, labs, theme, theme_minimal
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data
np.random.seed(42)
# Generate realistic height data (in cm) with slight bimodality
heights = np.concatenate(
    [
        np.random.normal(165, 7, 300),  # Female heights
        np.random.normal(178, 8, 300),  # Male heights
    ]
)
df = pd.DataFrame({"heights": heights})

# Plot
plot = (
    ggplot(df, aes(x="heights"))
    + geom_histogram(bins=30, fill="#306998", color="white", alpha=0.8, size=0.5)
    + labs(x="Height (cm)", y="Frequency", title="histogram-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(plot_title=element_text(size=24), axis_title=element_text(size=20), axis_text=element_text(size=16))
    + ggsize(1600, 900)
)

# Save PNG and HTML
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
