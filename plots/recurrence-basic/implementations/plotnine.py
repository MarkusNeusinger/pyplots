"""pyplots.ai
recurrence-basic: Recurrence Plot for Nonlinear Time Series
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-14
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_equal,
    element_blank,
    element_rect,
    element_text,
    geom_tile,
    ggplot,
    labs,
    scale_fill_gradientn,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from scipy.spatial.distance import cdist


# Data - Logistic map near onset of chaos (r=3.82)
np.random.seed(42)
n_steps = 300
r = 3.82
x = np.zeros(n_steps)
x[0] = 0.1
for i in range(1, n_steps):
    x[i] = r * x[i - 1] * (1 - x[i - 1])

# Time-delay embedding (dimension=3, delay=1)
embedding_dim = 3
delay = 1
n_embedded = n_steps - (embedding_dim - 1) * delay
embedded = np.array([x[i * delay : i * delay + n_embedded] for i in range(embedding_dim)]).T

# Distance matrix (Euclidean distance in embedding space)
distance_matrix = cdist(embedded, embedded, metric="euclidean")
threshold = 0.15

# Build long-form DataFrame with proximity (inverse distance) for color mapping
row_idx, col_idx = np.where(distance_matrix < threshold)
distances = distance_matrix[row_idx, col_idx]
proximity = 1.0 - distances / threshold  # 1.0 = exact match, 0.0 = at threshold

df = pd.DataFrame({"Time_i": row_idx, "Time_j": col_idx, "Proximity": proximity})

# Plot - distance-based color-mapped recurrence plot
plot = (
    ggplot(df, aes(x="Time_i", y="Time_j", fill="Proximity"))
    + geom_tile(width=1, height=1)
    + scale_fill_gradientn(
        colors=["#c7dcef", "#6baed6", "#2171b5", "#08306b"],
        name="Recurrence\nStrength",
        limits=(0, 1),
        breaks=[0, 0.25, 0.5, 0.75, 1.0],
        labels=["Weak", "", "Medium", "", "Strong"],
    )
    + scale_x_continuous(name="Time Step (Logistic Map, r = 3.82)", expand=(0, 0), breaks=range(0, n_embedded + 1, 50))
    + scale_y_continuous(name="Time Step (Logistic Map, r = 3.82)", expand=(0, 0), breaks=range(0, n_embedded + 1, 50))
    + coord_equal()
    + labs(title="recurrence-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(12, 12),
        text=element_text(family="sans-serif"),
        plot_title=element_text(size=26, ha="center", weight="bold", margin={"b": 12}),
        axis_title_x=element_text(size=22, margin={"t": 12}),
        axis_title_y=element_text(size=22, margin={"r": 12}),
        axis_text_x=element_text(size=17),
        axis_text_y=element_text(size=17),
        legend_title=element_text(size=18, weight="bold"),
        legend_text=element_text(size=16),
        legend_key_height=40,
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white", color="none"),
        plot_background=element_rect(fill="#fafaf7", color="none"),
        plot_margin=0.02,
    )
)

plot.save("plot.png", dpi=300, verbose=False)
