"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Plant growth measurements across different soil types
np.random.seed(42)

n_per_group = 40
categories = ["Sandy Soil", "Clay Soil", "Loamy Soil", "Peaty Soil"]

data = []
# Sandy soil - moderate growth, medium variation
data.extend([{"Soil Type": "Sandy Soil", "Plant Height (cm)": v} for v in np.random.normal(45, 8, n_per_group)])
# Clay soil - lower growth, tighter distribution
data.extend([{"Soil Type": "Clay Soil", "Plant Height (cm)": v} for v in np.random.normal(38, 5, n_per_group)])
# Loamy soil - best growth, wider spread with some outliers
loamy_vals = np.concatenate(
    [
        np.random.normal(62, 10, n_per_group - 3),
        np.array([85, 88, 25]),  # outliers
    ]
)
data.extend([{"Soil Type": "Loamy Soil", "Plant Height (cm)": v} for v in loamy_vals])
# Peaty soil - good growth, moderate variation
data.extend([{"Soil Type": "Peaty Soil", "Plant Height (cm)": v} for v in np.random.normal(55, 7, n_per_group)])

df = pd.DataFrame(data)

# Plot - Box plot with strip overlay
plot = (
    ggplot(df, aes(x="Soil Type", y="Plant Height (cm)"))
    + geom_boxplot(fill="#306998", color="#1a3d5c", alpha=0.6, width=0.6, size=1.2)
    + geom_jitter(color="#FFD43B", size=4, alpha=0.7, width=0.15)
    + labs(title="cat-box-strip · letsplot · pyplots.ai", x="Soil Type", y="Plant Height (cm)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale 3x for 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")
