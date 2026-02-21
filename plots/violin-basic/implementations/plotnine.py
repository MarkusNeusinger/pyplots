""" pyplots.ai
violin-basic: Basic Violin Plot
Library: plotnine 0.15.3 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_violin,
    ggplot,
    labs,
    scale_fill_brewer,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)

records = []

# Section A: right-skewed (many average, few high scorers)
scores_a = np.concatenate([np.random.normal(68, 6, 150), np.random.normal(85, 3, 30)])
records.extend([("Section A", s) for s in scores_a])

# Section B: bimodal (two clusters of performance)
scores_b = np.concatenate([np.random.normal(55, 5, 100), np.random.normal(82, 5, 100)])
records.extend([("Section B", s) for s in scores_b])

# Section C: tight normal (consistent performance)
scores_c = np.random.normal(74, 4, 200)
records.extend([("Section C", s) for s in scores_c])

# Section D: wide spread (high variance)
scores_d = np.random.normal(70, 14, 200)
records.extend([("Section D", s) for s in scores_d])

df = pd.DataFrame(records, columns=["section", "score"])
df["score"] = df["score"].clip(0, 100)

# Plot
plot = (
    ggplot(df, aes(x="section", y="score", fill="section"))
    + geom_violin(draw_quantiles=[0.25, 0.5, 0.75], size=0.8, trim=False)
    + scale_fill_brewer(type="qual", palette="Set2")
    + labs(x="Class Section", y="Exam Score (pts)", title="violin-basic \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
        panel_grid_major_x=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
