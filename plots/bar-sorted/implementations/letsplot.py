"""pyplots.ai
bar-sorted: Sorted Bar Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_flip,
    element_blank,
    element_line,
    element_text,
    geom_bar,
    ggplot,
    ggsize,
    labs,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Monthly revenue by product category in thousands (sorted descending)
data = {
    "Category": [
        "Electronics",
        "Clothing",
        "Home & Garden",
        "Sports",
        "Books",
        "Toys",
        "Beauty",
        "Automotive",
        "Food",
        "Health",
    ],
    "Revenue": [425, 312, 287, 198, 156, 142, 128, 95, 78, 62],  # in thousands
}
df = pd.DataFrame(data)

# Sort by revenue ascending so largest is at top after coord_flip
df = df.sort_values("Revenue", ascending=True)
df["Category"] = pd.Categorical(df["Category"], categories=df["Category"], ordered=True)

# Create sorted bar chart (horizontal for better label readability)
plot = (
    ggplot(df, aes(x="Category", y="Revenue"))
    + geom_bar(stat="identity", fill="#306998", width=0.7)
    + coord_flip()
    + scale_y_continuous(format="${}K")
    + labs(title="bar-sorted · lets-plot · pyplots.ai", x="Product Category", y="Monthly Revenue")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=26, face="bold"),
        axis_title_x=element_text(size=22),
        axis_title_y=element_text(size=22),
        axis_text_x=element_text(size=18),
        axis_text_y=element_text(size=18),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#CCCCCC", size=0.4, linetype="dashed"),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
