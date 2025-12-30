"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_jitter,
    ggplot,
    ggsize,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Product quality measurements across production lines
np.random.seed(42)

categories = ["Line A", "Line B", "Line C", "Line D", "Line E"]
n_per_category = 25

data = {"Production Line": [], "Quality Score": []}

# Create different distributions for each production line
distributions = {
    "Line A": (85, 5),  # High quality, consistent
    "Line B": (72, 8),  # Lower quality, more variable
    "Line C": (90, 3),  # Highest quality, very consistent
    "Line D": (78, 12),  # Medium quality, high variability
    "Line E": (82, 6),  # Good quality, moderate consistency
}

for cat in categories:
    mean, std = distributions[cat]
    values = np.random.normal(mean, std, n_per_category)
    values = np.clip(values, 50, 100)  # Keep scores realistic
    data["Production Line"].extend([cat] * n_per_category)
    data["Quality Score"].extend(values)

df = pd.DataFrame(data)

# Plot - Categorical strip plot with jitter
plot = (
    ggplot(df, aes(x="Production Line", y="Quality Score", color="Production Line"))
    + geom_jitter(size=5, alpha=0.7, width=0.25)
    + scale_color_manual(values=["#306998", "#FFD43B", "#2E7D32", "#D84315", "#6A1B9A"])
    + labs(title="cat-strip · letsplot · pyplots.ai", x="Production Line", y="Quality Score (%)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_position="none",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
