"""
density-basic: Basic Density Plot
Library: letsplot
"""

import numpy as np
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Generate realistic test scores with slight right skew
np.random.seed(42)
scores = np.concatenate(
    [
        np.random.normal(72, 12, 300),  # Main group of students
        np.random.normal(90, 5, 100),  # High achievers
    ]
)

# Create plot
plot = (
    ggplot({"scores": scores}, aes(x="scores"))  # noqa: F405
    + geom_density(fill="#306998", color="#306998", alpha=0.6, size=1.5)  # noqa: F405
    + labs(x="Test Score", y="Density", title="density-basic · letsplot · pyplots.ai")  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        panel_grid_major=element_line(color="#cccccc", size=0.5),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x for 4800x2700) and HTML to current directory
export_ggsave(plot, "plot.png", path=".", scale=3)
export_ggsave(plot, "plot.html", path=".")
