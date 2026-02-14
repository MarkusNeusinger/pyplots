""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotnine 0.15.3 | Python 3.14
Quality: 85/100 | Created: 2025-12-22
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_blank, element_line, element_text, geom_point, ggplot, labs, theme, theme_minimal


# Data: Study hours vs exam scores (realistic educational context)
np.random.seed(42)
n_points = 150
study_hours = np.random.uniform(1, 10, n_points)
exam_scores = 40 + study_hours * 5 + np.random.randn(n_points) * 8

df = pd.DataFrame({"study_hours": study_hours, "exam_scores": exam_scores})

# Plot
plot = (
    ggplot(df, aes(x="study_hours", y="exam_scores"))
    + geom_point(fill="#306998", color="white", shape="o", alpha=0.7, size=4, stroke=0.4)
    + labs(x="Study Hours (per week)", y="Exam Score (points)", title="scatter-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major=element_line(color="#d9d9d9", size=0.5),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
