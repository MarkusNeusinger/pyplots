"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_jitter, ggplot, labs, scale_color_manual, theme, theme_minimal


# Data
np.random.seed(42)

categories = ["Product A", "Product B", "Product C", "Product D"]
n_per_category = 30

data = []
# Different distributions for each category to show variation
distributions = {
    "Product A": (75, 8),  # mean=75, std=8
    "Product B": (82, 12),  # higher mean, more spread
    "Product C": (68, 6),  # lower mean, tighter
    "Product D": (78, 15),  # medium mean, widest spread
}

for cat in categories:
    mean, std = distributions[cat]
    values = np.random.normal(mean, std, n_per_category)
    for val in values:
        data.append({"Category": cat, "Performance Score": val})

df = pd.DataFrame(data)

# Color palette using Python colors
colors = ["#306998", "#FFD43B", "#306998", "#FFD43B"]

# Create plot
plot = (
    ggplot(df, aes(x="Category", y="Performance Score", color="Category"))
    + geom_jitter(size=4, alpha=0.7, width=0.25, height=0)
    + scale_color_manual(values=colors)
    + labs(x="Product Category", y="Performance Score", title="cat-strip · plotnine · pyplots.ai")
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
plot.save("plot.png", dpi=300)
