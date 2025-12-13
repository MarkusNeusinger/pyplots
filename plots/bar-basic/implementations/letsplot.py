"""
bar-basic: Basic Bar Chart
Library: lets-plot
"""

import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Product sales by category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food & Beverage"]
values = [45200, 32800, 28500, 21300, 18700, 15400, 12100]

df = pd.DataFrame({"category": categories, "value": values})

# Plot
plot = (
    ggplot(df, aes(x="category", y="value"))  # noqa: F405
    + geom_bar(stat="identity", fill="#306998", width=0.7)  # noqa: F405
    + labs(x="Product Category", y="Sales ($)", title="Product Sales by Category")  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text_x=element_text(angle=45, hjust=1, size=16),  # noqa: F405
        axis_text_y=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=20, hjust=0.5),  # noqa: F405
        panel_grid_major_x=element_blank(),  # noqa: F405
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
