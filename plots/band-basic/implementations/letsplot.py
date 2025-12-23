""" pyplots.ai
band-basic: Basic Band Plot
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
    element_text,
    geom_line,
    geom_ribbon,
    ggplot,
    ggsave,
    ggsize,
    labs,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_center = 2 * np.sin(x) + 0.5 * x  # Central trend (sinusoidal + linear growth)
noise_scale = 0.3 + 0.15 * x  # Increasing uncertainty over time
y_lower = y_center - 1.96 * noise_scale  # 95% CI lower bound
y_upper = y_center + 1.96 * noise_scale  # 95% CI upper bound

df = pd.DataFrame({"x": x, "y_center": y_center, "y_lower": y_lower, "y_upper": y_upper})

# Plot
plot = (
    ggplot(df, aes(x="x"))
    + geom_ribbon(aes(ymin="y_lower", ymax="y_upper"), fill="#306998", alpha=0.3)
    + geom_line(aes(y="y_center"), color="#306998", size=1.5)
    + labs(x="Time (s)", y="Value (units)", title="band-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid=element_line(color="#cccccc", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")
