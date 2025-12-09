"""
box-basic: Basic Box Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_boxplot, ggplot, labs, scale_fill_manual, theme, theme_minimal


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create plot
plot = (
    ggplot(data, aes(x="group", y="value", fill="group"))
    + geom_boxplot(alpha=0.8, outlier_alpha=0.6)
    + scale_fill_manual(values=colors)
    + labs(x="Group", y="Value", title="Basic Box Plot")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=16),
        legend_text=element_text(size=16),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300)
