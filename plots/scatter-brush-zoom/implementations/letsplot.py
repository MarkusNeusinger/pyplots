""" pyplots.ai
scatter-brush-zoom: Interactive Scatter Plot with Brush Selection and Zoom
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 65/100 | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Generate clustered data for brush selection demonstration
np.random.seed(42)

# Create 4 distinct clusters with different sizes
n_per_cluster = [80, 120, 100, 100]
centers = [(20, 60), (50, 30), (70, 70), (40, 80)]
spreads = [8, 12, 10, 6]
categories = ["Cluster A", "Cluster B", "Cluster C", "Cluster D"]

x_data, y_data, colors = [], [], []
for n, (cx, cy), spread, cat in zip(n_per_cluster, centers, spreads, categories):
    x_data.extend(np.random.normal(cx, spread, n))
    y_data.extend(np.random.normal(cy, spread, n))
    colors.extend([cat] * n)

df = pd.DataFrame({"x": x_data, "y": y_data, "category": colors})

# Add point labels for subset of points
df["label"] = [f"P{i}" if i % 50 == 0 else "" for i in range(len(df))]

# Create interactive scatter plot with brush selection and zoom
plot = (
    ggplot(df, aes(x="x", y="y", color="category"))
    + geom_point(size=5, alpha=0.7, show_legend=True)
    + scale_color_manual(values=["#306998", "#FFD43B", "#DC2626", "#059669"])
    + labs(x="X Value", y="Y Value", title="scatter-brush-zoom · letsplot · pyplots.ai", color="Category")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
    )
    + ggsize(1600, 900)
)

# Save static PNG (scaled 3x for 4800x2700 px) - path="." saves to current directory
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML with brush and zoom capabilities
# lets-plot HTML export includes built-in pan and zoom functionality
ggsave(plot, "plot.html", path=".")
