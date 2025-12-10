"""
violin-basic: Basic Violin Plot
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_boxplot,
    geom_violin,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Employee performance scores grouped by department
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "Support", "Finance"]
data = []

for dept in departments:
    if dept == "Engineering":
        scores = np.random.normal(75, 10, 120)
    elif dept == "Marketing":
        scores = np.random.normal(70, 15, 100)
    elif dept == "Sales":
        scores = np.concatenate([np.random.normal(60, 8, 60), np.random.normal(85, 5, 40)])
    elif dept == "Support":
        scores = np.random.normal(72, 12, 90)
    else:  # Finance
        scores = np.random.normal(78, 8, 80)

    scores = np.clip(scores, 30, 100)
    for score in scores:
        data.append({"Department": dept, "Performance Score": score})

df = pd.DataFrame(data)

# Define colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Create violin plot
plot = (
    ggplot(df, aes(x="Department", y="Performance Score", fill="Department"))
    + geom_violin(alpha=0.8, trim=False, show_legend=False)
    + geom_boxplot(width=0.1, fill="white", alpha=0.7, outlier_shape=21, outlier_size=2)
    + scale_fill_manual(values=colors)
    + labs(title="Employee Performance Score Distribution by Department", x="Department", y="Performance Score")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=20),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(angle=0),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x to get 4800 × 2700 px)
ggsave(plot, "plot.png", scale=3, path=".")

# Save as HTML for interactive viewing
ggsave(plot, "plot.html", path=".")
