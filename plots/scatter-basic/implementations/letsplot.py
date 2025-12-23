""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: letsplot unknown | Python 3.13.11
Quality: 90/100 | Created: 2025-12-22
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Simulating study hours vs exam scores relationship
np.random.seed(42)
n = 120
study_hours = np.random.uniform(1, 10, n)
exam_scores = study_hours * 8 + 20 + np.random.randn(n) * 5

df = pd.DataFrame({"study_hours": study_hours, "exam_scores": exam_scores})

# Plot with interactive tooltips
plot = (
    ggplot(df, aes(x="study_hours", y="exam_scores"))  # noqa: F405
    + geom_point(  # noqa: F405
        color="#306998",
        size=6,
        alpha=0.7,
        tooltips=layer_tooltips()  # noqa: F405
        .line("Study Hours|@study_hours")
        .line("Exam Score|@exam_scores"),
    )
    + labs(  # noqa: F405
        x="Study Hours (hrs)", y="Exam Score (points)", title="scatter-basic · letsplot · pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
