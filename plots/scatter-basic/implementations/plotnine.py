""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-13
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_point, ggplot, labs, theme, theme_minimal


# Data
np.random.seed(42)
n_points = 150
x = np.random.randn(n_points) * 2 + 10
y = x * 0.8 + np.random.randn(n_points) * 2

df = pd.DataFrame({"x": x, "y": y})

# Plot
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_point(color="#306998", alpha=0.7, size=4)
    + labs(x="X Value", y="Y Value", title="scatter-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
