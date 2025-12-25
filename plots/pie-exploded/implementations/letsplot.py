"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Budget allocation by department with R&D (highest) and Sales emphasized
categories = ["Marketing", "Operations", "R&D", "Sales", "HR", "IT"]
values = [18, 15, 32, 20, 8, 7]
# Explode R&D (largest, index 2) and Sales (emphasis, index 3)
explode = [0, 0, 0.15, 0.1, 0, 0]

df = pd.DataFrame({"category": categories, "value": values, "explode": explode})

# Calculate percentages for labels
total = sum(values)
df["pct"] = df["value"] / total * 100

# Preserve category order
df["category"] = pd.Categorical(df["category"], categories=categories, ordered=True)

# Define colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4CAF50", "#FF7043", "#AB47BC", "#42A5F5"]

# Plot - lets-plot geom_pie supports explode parameter
plot = (
    ggplot(df)  # noqa: F405
    + geom_pie(  # noqa: F405
        aes(slice="value", fill="category", explode="explode"),  # noqa: F405
        stat="identity",
        size=38,  # Larger size for better canvas utilization
        hole=0,  # Full pie (not donut)
        stroke=1.5,  # Add edge definition
        labels=layer_labels()  # noqa: F405
        .line("@pct")
        .format("pct", "{.1f}%")
        .size(18),
    )
    + scale_fill_manual(values=colors)  # noqa: F405
    + labs(  # noqa: F405
        title="pie-exploded · letsplot · pyplots.ai", fill="Department"
    )
    + ggsize(1200, 1200)  # noqa: F405  # Square for pie (scale 3x = 3600x3600)
    + theme_void()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=28, hjust=0.5),  # noqa: F405
        legend_title=element_text(size=20),  # noqa: F405
        legend_text=element_text(size=18),  # noqa: F405
        legend_position=[0.85, 0.5],  # Position legend to the right
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
