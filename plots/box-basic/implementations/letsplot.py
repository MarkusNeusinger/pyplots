""" pyplots.ai
box-basic: Basic Box Plot
Library: letsplot unknown | Python 3.13.11
Quality: 98/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
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
# Realistic salary distributions for each department
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
    # Add a few outliers
    outliers = np.random.choice([mean + 3.5 * std, mean - 2.5 * std], size=3)
    values = np.concatenate([values, outliers])
    data.extend([(cat, v) for v in values])

df = pd.DataFrame(data, columns=["category", "value"])

# Plot
colors = ["#306998", "#FFD43B", "#DC2626", "#16A34A", "#9333EA"]

plot = (
    ggplot(df, aes(x="category", y="value", fill="category"))
    + geom_boxplot(alpha=0.8, size=1.5, outlier_size=4)
    + scale_fill_manual(values=colors)
    + labs(x="Department", y="Salary ($)", title="box-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
