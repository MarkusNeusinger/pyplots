"""
donut-labeled: Donut Chart with Percentage Labels
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
    layer_labels,
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

# Data - Department budget allocation
data = pd.DataFrame(
    {"category": ["Marketing", "Engineering", "Operations", "Sales", "HR", "R&D"], "value": [25, 30, 15, 18, 7, 5]}
)

# Calculate percentages for labels
total = data["value"].sum()
data["percentage"] = (data["value"] / total * 100).round(1)
data["label"] = data["percentage"].astype(str) + "%"

# Create donut chart with hole parameter and percentage labels using layer_labels
plot = (
    ggplot(data)
    + geom_pie(
        aes(fill="category", slice="value"),
        stat="identity",
        hole=0.5,  # Inner radius for donut appearance
        stroke=1.5,
        color="white",
        stroke_side="both",
        size=16,
        labels=layer_labels().line("@label").size(14).format("@label", "{}"),
        tooltips="none",
    )
    + scale_fill_manual(values=PYPLOTS_COLORS)
    + labs(title="Department Budget Allocation", fill="Department")
    + theme_void()
    + theme(
        plot_title=element_text(size=20, face="bold", hjust=0.5),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save PNG - scale 3x to get 4800 x 2700 px
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive viewing
ggsave(plot, "plot.html", path=".")
