"""
scatter-basic: Basic Scatter Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, geom_point, ggplot, labs, theme, theme_minimal


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

df = pd.DataFrame({"x": x, "y": y})

# Plot
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_point(alpha=0.7, size=3, color="#306998")
    + labs(x="X Value", y="Y Value", title="Basic Scatter Plot")
    + theme_minimal()
    + theme(figure_size=(16, 9))
)

# Save
plot.save("plot.png", dpi=300)
