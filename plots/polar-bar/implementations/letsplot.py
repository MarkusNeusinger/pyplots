"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Wind direction frequency (8 compass directions)
np.random.seed(42)
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
# Wind frequency with realistic variation (prevailing westerlies)
frequencies = [15, 8, 12, 5, 7, 18, 25, 20]

df = pd.DataFrame(
    {
        "direction": directions,
        "frequency": frequencies,
        "angle": np.arange(0, 360, 45),  # Angle for each direction
    }
)

# Plot - Polar bar chart using coord_polar
plot = (
    ggplot(df, aes(x="direction", y="frequency", fill="direction"))
    + geom_bar(stat="identity", width=0.8, alpha=0.85)
    + coord_polar()
    + scale_fill_manual(
        values=[
            "#306998",  # N - Python Blue
            "#FFD43B",  # NE - Python Yellow
            "#4A90D9",  # E
            "#6DB33F",  # SE
            "#9B59B6",  # S
            "#E67E22",  # SW
            "#1ABC9C",  # W
            "#E74C3C",  # NW
        ]
    )
    + scale_x_discrete(limits=["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    + labs(title="polar-bar · lets-plot · pyplots.ai", x="", y="Frequency (%)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_text=element_text(size=16),
        axis_title_y=element_text(size=18),
        legend_position="none",
        panel_grid_major=element_line(color="#CCCCCC", size=0.3),
    )
    + ggsize(1200, 1200)  # Square for polar chart (scaled 3x = 3600x3600)
)

# Save as PNG and HTML (to current directory)
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
