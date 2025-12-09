"""
ridgeline-basic: Ridgeline Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    facet_wrap,
    geom_density,
    ggplot,
    labs,
    scale_fill_manual,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Monthly temperature readings
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
n_per_month = 100

# Generate temperature data with seasonal pattern
data_list = []
base_temps = [2, 4, 8, 12, 17, 21, 24, 23, 19, 13, 7, 3]  # Typical seasonal pattern

for i, month in enumerate(months):
    temps = np.random.normal(base_temps[i], 3, n_per_month)
    data_list.append(pd.DataFrame({"month": month, "temperature": temps}))

data = pd.concat(data_list, ignore_index=True)

# Convert month to ordered categorical (reversed for ridgeline stacking - Dec at top)
data["month"] = pd.Categorical(data["month"], categories=months[::-1], ordered=True)

# Create gradient colors from cool to warm (matching seasonal pattern)
colors = {
    "Jan": "#306998",
    "Feb": "#3B7AAD",
    "Mar": "#4D8BC2",
    "Apr": "#5F9CD7",
    "May": "#71ADEC",
    "Jun": "#FFD43B",
    "Jul": "#F97316",
    "Aug": "#DC2626",
    "Sep": "#F97316",
    "Oct": "#FFD43B",
    "Nov": "#71ADEC",
    "Dec": "#306998",
}

# Create ridgeline plot using facet_wrap for vertical stacking
plot = (
    ggplot(data, aes(x="temperature", fill="month"))
    + geom_density(alpha=0.7, color="white", size=0.5)
    + facet_wrap("~month", ncol=1, scales="free_y")
    + scale_fill_manual(values=colors)
    + labs(x="Temperature (\u00b0C)", y="", title="Monthly Temperature Distribution")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20),
        axis_title_x=element_text(size=20),
        axis_text_x=element_text(size=16),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        strip_text=element_text(size=14),
        strip_background=element_blank(),
        legend_position="none",
        panel_spacing_y=-0.3,
        panel_grid=element_blank(),
        axis_line_x=element_line(color="#333333", size=0.5),
    )
    + scale_y_continuous(expand=(0, 0))
)

# Save
plot.save("plot.png", dpi=300)
