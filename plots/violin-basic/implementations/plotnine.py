"""
violin-basic: Basic Violin Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_violin, ggplot, labs, scale_fill_manual, theme, theme_minimal


# Data
np.random.seed(42)

categories = ["Group A", "Group B", "Group C", "Group D"]
data = []

# Generate data with different distributions for each category
distributions = {
    "Group A": (50, 10),  # mean, std
    "Group B": (65, 15),
    "Group C": (45, 8),
    "Group D": (70, 12),
}

for category, (mean, std) in distributions.items():
    n_points = 200
    values = np.random.normal(mean, std, n_points)
    data.extend([(category, v) for v in values])

df = pd.DataFrame(data, columns=["category", "value"])

# Plot
plot = (
    ggplot(df, aes(x="category", y="value", fill="category"))
    + geom_violin(draw_quantiles=[0.25, 0.5, 0.75], size=1)
    + scale_fill_manual(values=["#306998", "#FFD43B", "#4B8BBE", "#FFE873"])
    + labs(x="Category", y="Value", title="violin-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
