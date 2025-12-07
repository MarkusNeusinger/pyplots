"""
pie-basic: Basic Pie Chart
Library: lets-plot
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_pie,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    theme_void,
)


LetsPlot.setup_html()

# PyPlots.ai color palette
PYPLOTS_COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]

# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Create pie chart
plot = (
    ggplot(data)
    + geom_pie(aes(slice="value", fill="category"), stat="identity", stroke=1.5, color="white", size=20)
    + scale_fill_manual(values=PYPLOTS_COLORS)
    + labs(title="Market Share Distribution", fill="Category")
    + theme_void()
    + theme(
        plot_title=element_text(size=20, face="bold", hjust=0.5),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save - scale 3x to get 4800 x 2700 px
ggsave(plot, "plot.png", path=".", scale=3)
