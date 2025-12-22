"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-22
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data
np.random.seed(42)
n = 150
x = np.random.randn(n) * 2 + 10
y = x * 0.8 + np.random.randn(n) * 2

df = pd.DataFrame({"x": x, "y": y})

# Plot
plot = (
    ggplot(df, aes(x="x", y="y"))  # noqa: F405
    + geom_point(color="#306998", size=5, alpha=0.7)  # noqa: F405
    + labs(  # noqa: F405
        x="X Value", y="Y Value", title="scatter-basic \u00b7 lets-plot \u00b7 pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
