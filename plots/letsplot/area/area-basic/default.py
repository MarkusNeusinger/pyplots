"""
area-basic: Basic Area Chart
Library: letsplot
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_area,
    geom_line,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_x_continuous,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
data = pd.DataFrame(
    {"month_num": range(len(months)), "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190]}
)

# Plot
plot = (
    ggplot(data, aes(x="month_num", y="sales"))
    + geom_area(fill="#306998", alpha=0.5)
    + geom_line(color="#306998", size=2)
    + scale_x_continuous(breaks=list(range(len(months))), labels=months)
    + labs(x="Month", y="Sales", title="Basic Area Chart")
    + theme_minimal()
    + theme(axis_title=element_text(size=20), axis_text=element_text(size=16), plot_title=element_text(size=20))
    + ggsize(1600, 900)
)

# Save - scale 3x to get 4800 × 2700 px
ggsave(plot, "plot.png", path=".", scale=3)
