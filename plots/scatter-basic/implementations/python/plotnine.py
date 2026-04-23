"""anyplot.ai
scatter-basic: Basic Scatter Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-04-23
"""

import os

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_point,
    ggplot,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
RULE_ALPHA = 0.10
BRAND = "#009E73"

# Data: study hours vs exam scores, moderate positive correlation with noise
np.random.seed(42)
n_points = 150
study_hours = np.random.uniform(1, 10, n_points)
base_scores = 32 + study_hours * 5.5 + 0.35 * (study_hours - 5) ** 2
noise = np.random.randn(n_points) * 8
exam_scores = np.clip(base_scores + noise, 15, 100)

df = pd.DataFrame({"study_hours": study_hours, "exam_scores": exam_scores})

# Plot
plot = (
    ggplot(df, aes(x="study_hours", y="exam_scores"))
    + geom_point(color=BRAND, fill=BRAND, alpha=0.7, size=4, stroke=0.4)
    + scale_x_continuous(breaks=range(1, 11), limits=(0.5, 10.5))
    + scale_y_continuous(breaks=range(20, 101, 20), limits=(10, 105))
    + labs(x="Study Hours per Week", y="Exam Score (points)", title="scatter-basic · plotnine · anyplot.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color=INK_SOFT),
        axis_title=element_text(size=20, color=INK),
        axis_text=element_text(size=16, color=INK_SOFT),
        plot_title=element_text(size=24, color=INK, ha="left", margin={"b": 18}),
        plot_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
        panel_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
        panel_grid_major=element_line(color=INK, size=0.35, alpha=RULE_ALPHA),
        panel_grid_minor=element_blank(),
        axis_line=element_line(color=INK_SOFT, size=0.6),
        axis_ticks=element_blank(),
        panel_border=element_blank(),
    )
)

# Save
plot.save(f"plot-{THEME}.png", dpi=300, verbose=False)
