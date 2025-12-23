"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    labs,
    scale_fill_gradient2,
    theme,
    theme_minimal,
)


# Data - 8x8 matrix with meaningful patterns (performance metrics by region and quarter)
np.random.seed(42)
rows = ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G", "Region H"]
cols = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]

# Create data with a trend and variation
base_values = np.linspace(-30, 40, 8)  # Trend across columns
row_effects = np.random.uniform(-10, 10, 8)  # Row-specific offsets
values = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        values[i, j] = base_values[j] + row_effects[i] + np.random.uniform(-8, 8)

# Create long-form DataFrame for plotnine
data = []
for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        data.append({"x": col, "y": row, "value": round(values[i, j], 1)})

df = pd.DataFrame(data)

# Preserve ordering
df["x"] = pd.Categorical(df["x"], categories=cols, ordered=True)
df["y"] = pd.Categorical(df["y"], categories=rows[::-1], ordered=True)  # Reverse for top-to-bottom

# Plot
plot = (
    ggplot(df, aes(x="x", y="y", fill="value"))
    + geom_tile(color="white", size=0.5)
    + geom_text(aes(label="value"), size=12, color="black")
    + scale_fill_gradient2(
        low="#306998",  # Python Blue for negative
        mid="white",
        high="#FFD43B",  # Python Yellow for positive
        midpoint=0,
        name="Value",
    )
    + labs(x="Time Period", y="Region", title="heatmap-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text_x=element_text(size=14, rotation=45, ha="right"),
        axis_text_y=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
