""" pyplots.ai
box-basic: Basic Box Plot
Library: letsplot 4.8.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    as_discrete,
    element_blank,
    element_line,
    element_text,
    geom_boxplot,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
data = []
distributions = {
    "Engineering": (85000, 15000),
    "Marketing": (65000, 12000),
    "Sales": (70000, 20000),
    "HR": (55000, 10000),
    "Finance": (75000, 14000),
}

for cat in categories:
    mean, std = distributions[cat]
    n = np.random.randint(50, 100)
    values = np.random.normal(mean, std, n)
    outliers = np.random.choice([mean + 3.5 * std, mean - 2.5 * std], size=3)
    values = np.concatenate([values, outliers])
    data.extend([(cat, v) for v in values])

df = pd.DataFrame(data, columns=["department", "salary"])

# Plot
colors = ["#306998", "#E69F00", "#56B4E9", "#009E73", "#CC79A7"]

plot = (
    ggplot(df, aes(x=as_discrete("department", order=1, order_by="..middle.."), y="salary", fill="department"))
    + geom_boxplot(alpha=0.85, size=1.2, outlier_size=4, outlier_shape=21, outlier_fill="#555555", width=0.65)
    + scale_fill_manual(values=colors)
    + labs(x="Department", y="Salary ($)", title="box-basic \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_ticks=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#CCCCCC", size=0.6),
        legend_position="none",
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
