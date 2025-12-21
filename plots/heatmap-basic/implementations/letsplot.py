""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-14
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    ggsize,
    labs,
    scale_fill_gradient2,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Create a correlation-style matrix with meaningful labels
np.random.seed(42)
categories_x = ["Sales", "Marketing", "R&D", "Operations", "Finance", "HR"]
categories_y = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]

# Generate performance scores (0-100 range with some variation)
n_rows = len(categories_y)
n_cols = len(categories_x)
values = np.random.rand(n_rows, n_cols) * 60 + 20  # Range 20-80
values = np.round(values, 1)

# Create long-form DataFrame for lets-plot
rows = []
for i, y_cat in enumerate(categories_y):
    for j, x_cat in enumerate(categories_x):
        rows.append({"x": x_cat, "y": y_cat, "value": values[i, j]})

df = pd.DataFrame(rows)

# Preserve category order
df["x"] = pd.Categorical(df["x"], categories=categories_x, ordered=True)
df["y"] = pd.Categorical(df["y"], categories=categories_y[::-1], ordered=True)

# Create heatmap using geom_tile
plot = (
    ggplot(df, aes(x="x", y="y", fill="value"))
    + geom_tile(width=0.95, height=0.95)
    + geom_text(aes(label="value"), size=14, color="white", fontface="bold")
    + scale_fill_gradient2(low="#306998", mid="#FFD43B", high="#DC2626", midpoint=50, name="Score")
    + labs(x="Department", y="Quarter", title="heatmap-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(angle=45),
        plot_title=element_text(size=24),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
