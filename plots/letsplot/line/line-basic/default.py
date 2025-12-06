"""
line-basic: Basic Line Plot
Library: letsplot
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

# Plot
plot = (
    ggplot(data, aes(x="time", y="value"))
    + geom_line(color="#306998", size=2, alpha=1.0)
    + geom_point(color="#306998", size=4, alpha=1.0)
    + labs(x="Time", y="Value", title="Basic Line Plot")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=20, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#CCCCCC", size=0.5),
        panel_grid_minor=element_line(color="#EEEEEE", size=0.3),
    )
    + ggsize(1600, 900)
)

# Save - scale 3x to get 4800 x 2700 px
ggsave(plot, "plot.png", path=".", scale=3)
