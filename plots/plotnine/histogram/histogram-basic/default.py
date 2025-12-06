"""
histogram-basic: Basic Histogram
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_histogram, ggplot, labs, theme, theme_minimal


# Data
np.random.seed(42)
data = pd.DataFrame({"value": np.random.normal(100, 15, 500)})

# Plot
plot = (
    ggplot(data, aes(x="value"))
    + geom_histogram(bins=30, fill="#306998", color="white", alpha=0.8)
    + labs(x="Value", y="Frequency", title="Basic Histogram")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
    )
)

# Save
plot.save("plot.png", dpi=300)
