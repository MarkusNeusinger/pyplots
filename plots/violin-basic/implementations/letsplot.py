""" pyplots.ai
violin-basic: Basic Violin Plot
Library: letsplot 4.8.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales", "Design"]
colors = ["#306998", "#E8A317", "#4B8BBE", "#2E8B57"]

data = []
distributions = {
    "Engineering": {"mean": 95000, "std": 20000, "n": 200},
    "Marketing": {"mean": 75000, "std": 15000, "n": 150},
    "Sales": {"mean": 70000, "std": 25000, "n": 180},
    "Design": {"mean": 80000, "std": 18000, "n": 120},
}

for cat in categories:
    dist = distributions[cat]
    values = np.random.normal(dist["mean"], dist["std"], dist["n"])
    values = np.clip(values, 30000, 200000)
    for v in values:
        data.append({"Department": cat, "Salary": v})

df = pd.DataFrame(data)

# Plot
plot = (
    ggplot(df, aes(x="Department", y="Salary", fill="Department"))  # noqa: F405
    + geom_violin(  # noqa: F405
        quantiles=[0.25, 0.5, 0.75], quantile_lines=True, size=1.2, alpha=0.85, trim=False, color="#2C3E50"
    )
    + scale_fill_manual(values=colors)  # noqa: F405
    + scale_y_continuous(  # noqa: F405
        format="${,.0f}"
    )
    + labs(  # noqa: F405
        x="Department", y="Salary", title="violin-basic \u00b7 letsplot \u00b7 pyplots.ai"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        legend_position="none",
        panel_grid_major_x=element_blank(),  # noqa: F405
        axis_ticks=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
