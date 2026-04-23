""" anyplot.ai
scatter-basic: Basic Scatter Plot
Library: plotnine 0.15.3 | Python 3.14.4
Quality: 87/100 | Created: 2026-04-23
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
    theme,
    theme_minimal,
)


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = INK
GRID_ALPHA = 0.10
BRAND = "#009E73"

# Data
np.random.seed(42)
n_points = 180
study_hours = np.random.uniform(1, 10, n_points)
base_scores = 32 + study_hours * 6
noise = np.random.randn(n_points) * 7
exam_scores = np.clip(base_scores + noise, 15, 100)
df = pd.DataFrame({"study_hours": study_hours, "exam_scores": exam_scores})

# Plot
plot = (
    ggplot(df, aes(x="study_hours", y="exam_scores"))
    + geom_point(color=BRAND, fill=BRAND, alpha=0.70, size=4.0, stroke=0.4)
    + labs(x="Study Hours (per week)", y="Exam Score (points)", title="scatter-basic · plotnine · anyplot.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color=INK_SOFT),
        plot_title=element_text(size=24, color=INK, ha="left", margin={"b": 16}),
        axis_title_x=element_text(size=20, color=INK, margin={"t": 12}),
        axis_title_y=element_text(size=20, color=INK, margin={"r": 12}),
        axis_text=element_text(size=16, color=INK_SOFT),
        axis_ticks=element_blank(),
        axis_line=element_line(color=INK_SOFT, size=0.6),
        panel_grid_major=element_line(color=GRID, size=0.4, alpha=GRID_ALPHA),
        panel_grid_minor=element_blank(),
        plot_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
        panel_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
    )
)

# Save
plot.save(f"plot-{THEME}.png", dpi=300, verbose=False)
