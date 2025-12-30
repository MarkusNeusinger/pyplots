""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Plant growth measurements across different fertilizer treatments
np.random.seed(42)

categories = ["Control", "Nitrogen", "Phosphorus", "Potassium", "Complete"]
n_per_group = 25

data = []
# Different distributions for each treatment group to show variation
distributions = {
    "Control": (15, 3),  # Low growth, low variance
    "Nitrogen": (25, 4),  # Moderate growth
    "Phosphorus": (22, 5),  # Moderate growth, more variance
    "Potassium": (20, 3.5),  # Moderate-low growth
    "Complete": (32, 6),  # High growth, high variance (includes some outliers)
}

for cat in categories:
    mean, std = distributions[cat]
    values = np.random.normal(mean, std, n_per_group)
    # Add a few outliers for Complete fertilizer
    if cat == "Complete":
        values[0] = 48  # High outlier
        values[1] = 12  # Low outlier
    for v in values:
        data.append({"Fertilizer": cat, "Growth (cm)": v})

df = pd.DataFrame(data)

# Plot - strip plot with jitter
plot = (
    ggplot(df, aes(x="Fertilizer", y="Growth (cm)", color="Fertilizer"))
    + geom_jitter(size=4, alpha=0.7, width=0.25, height=0)
    + scale_color_manual(values=["#306998", "#FFD43B", "#22C55E", "#A855F7", "#EF4444"])
    + labs(title="cat-strip · letsplot · pyplots.ai", x="Fertilizer Treatment", y="Plant Growth (cm)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="none",  # Category already shown on x-axis
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save - use path= to avoid subdirectory creation
ggsave(plot, "plot.png", path=".", scale=3)

# Also save HTML for interactive version
ggsave(plot, "plot.html", path=".")
