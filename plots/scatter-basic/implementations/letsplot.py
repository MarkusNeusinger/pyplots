"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-22
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Study Hours vs Exam Scores (realistic educational context)
np.random.seed(42)
n = 120
study_hours = np.random.uniform(1, 12, n)
base_score = 40 + study_hours * 4.5  # Linear relationship
noise = np.random.randn(n) * 8  # Natural variation
exam_scores = np.clip(base_score + noise, 0, 100)  # Bound between 0-100

df = pd.DataFrame({"study_hours": study_hours, "exam_scores": exam_scores})

# Plot
plot = (
    ggplot(df, aes(x="study_hours", y="exam_scores"))  # noqa: F405
    + geom_point(color="#306998", size=5, alpha=0.7)  # noqa: F405
    + labs(  # noqa: F405
        x="Study Hours per Day", y="Exam Score (%)", title="scatter-basic · letsplot · pyplots.ai"
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

# Save PNG (scale 3x to get 4800 × 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
