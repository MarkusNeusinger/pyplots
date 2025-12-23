"""pyplots.ai
violin-basic: Basic Violin Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales", "Design"]
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]

# Generate realistic salary distributions per department
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
    values = np.clip(values, 30000, 200000)  # Realistic salary bounds
    for v in values:
        data.append({"Department": cat, "Salary": v})

df = pd.DataFrame(data)

# Plot
plot = (
    ggplot(df, aes(x="Department", y="Salary", fill="Department"))  # noqa: F405
    + geom_violin(  # noqa: F405
        quantiles=[0.25, 0.5, 0.75],  # Show quartiles including median
        quantile_lines=True,  # Draw lines at quantiles
        size=1.5,  # Border thickness
        alpha=0.8,
        trim=False,  # Show full tails
    )
    + scale_fill_manual(values=colors)  # noqa: F405
    + labs(  # noqa: F405
        x="Department", y="Salary ($)", title="violin-basic · lets-plot · pyplots.ai"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        legend_position="none",  # Legend not needed, x-axis shows categories
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x to get 4800 × 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
