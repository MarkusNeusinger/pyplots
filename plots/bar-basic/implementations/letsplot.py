""" pyplots.ai
bar-basic: Basic Bar Chart
Library: letsplot 4.8.2 | Python 3.14
Quality: 83/100 | Created: 2025-12-23
"""

import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Product sales by category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [45200, 32800, 28500, 21300, 18900, 15600]

df = pd.DataFrame({"category": categories, "value": values})

# Plot
plot = (
    ggplot(df, aes(x="category", y="value"))  # noqa: F405
    + geom_bar(stat="identity", fill="#306998", width=0.6)  # noqa: F405
    + geom_text(  # noqa: F405
        aes(label="value"),  # noqa: F405
        position=position_nudge(y=1500),  # noqa: F405
        size=14,
        label_format="${,d}",
    )
    + labs(  # noqa: F405
        x="Product Category", y="Sales ($)", title="bar-basic · letsplot · pyplots.ai"
    )
    + scale_x_discrete(limits=categories)  # noqa: F405
    + scale_y_continuous(  # noqa: F405
        limits=[0, 55000],
        breaks=[0, 10000, 20000, 30000, 40000, 50000],
        labels=["$0K", "$10K", "$20K", "$30K", "$40K", "$50K"],
    )
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        axis_text_x=element_text(angle=45, hjust=1, size=16),  # noqa: F405
        axis_text_y=element_text(size=16),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        plot_title=element_text(size=24, hjust=0.5),  # noqa: F405
        panel_grid_major_x=element_blank(),  # noqa: F405
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
