"""
bubble-basic: Basic Bubble Chart
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_point, ggplot, labs, scale_size_area, theme, theme_minimal


# Data
np.random.seed(42)
n_points = 50
x = np.random.randn(n_points) * 2 + 10
y = x * 0.6 + np.random.randn(n_points) * 1.5 + 5
size = np.random.uniform(10, 100, n_points)

df = pd.DataFrame({"x": x, "y": y, "size": size})

# Plot
plot = (
    ggplot(df, aes(x="x", y="y", size="size"))
    + geom_point(color="#306998", alpha=0.6)
    + scale_size_area(max_size=20, name="Size")
    + labs(x="X Value", y="Y Value", title="bubble-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
