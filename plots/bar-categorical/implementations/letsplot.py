"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - raw categorical values (counts computed automatically by geom_bar)
np.random.seed(42)
categories = ["Apples", "Bananas", "Oranges", "Grapes", "Mangoes"]
weights = [0.25, 0.20, 0.22, 0.18, 0.15]
n_samples = 200

df = pd.DataFrame({"fruit": np.random.choice(categories, size=n_samples, p=weights)})

# Plot - geom_bar computes counts automatically (no stat='identity')
plot = (
    ggplot(df, aes(x="fruit"))  # noqa: F405
    + geom_bar(fill="#306998", color="#1a3a54", size=0.5, alpha=0.9)  # noqa: F405
    + labs(  # noqa: F405
        x="Fruit Type", y="Count", title="bar-categorical · letsplot · pyplots.ai"
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        axis_text_x=element_text(angle=0),  # noqa: F405
        panel_grid_major_x=element_blank(),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
)

# Save as PNG (scale 3x for 4800x2700 px) and HTML
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
