""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
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

# Data - Department performance scores by quarter
np.random.seed(42)
departments = ["Sales", "Marketing", "R&D", "Operations", "Finance", "HR"]
quarters = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]

# Generate performance scores with some patterns
n_rows = len(quarters)
n_cols = len(departments)
base_scores = np.random.rand(n_rows, n_cols) * 60 + 20  # Range 20-80

# Add some trend patterns to make data more interesting
trend = np.linspace(0, 15, n_rows).reshape(-1, 1)  # Slight upward trend
values = base_scores + trend
values = np.clip(values, 15, 95)  # Keep in realistic range
values = np.round(values, 1)

# Create long-form DataFrame for lets-plot
rows = []
for i, quarter in enumerate(quarters):
    for j, dept in enumerate(departments):
        rows.append({"Department": dept, "Quarter": quarter, "Score": values[i, j]})

df = pd.DataFrame(rows)

# Preserve category order (reverse quarters for top-to-bottom display)
df["Department"] = pd.Categorical(df["Department"], categories=departments, ordered=True)
df["Quarter"] = pd.Categorical(df["Quarter"], categories=quarters[::-1], ordered=True)

# Create heatmap using geom_tile with value annotations
plot = (
    ggplot(df, aes(x="Department", y="Quarter", fill="Score"))
    + geom_tile(width=0.95, height=0.95)
    + geom_text(aes(label="Score"), size=14, color="white", fontface="bold")
    + scale_fill_gradient2(low="#306998", mid="#FFD43B", high="#DC2626", midpoint=55, name="Performance\nScore")
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
