"""
bar-basic: Basic Bar Chart
Library: letsplot
"""

import pandas as pd
from lets_plot import LetsPlot, aes, element_text, geom_bar, ggplot, ggsave, ggsize, labs, theme, theme_minimal


LetsPlot.setup_html()

# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Plot
plot = (
    ggplot(data, aes(x="category", y="value"))
    + geom_bar(stat="identity", fill="#306998", alpha=0.9)
    + labs(x="Category", y="Value", title="Basic Bar Chart")
    + theme_minimal()
    + theme(plot_title=element_text(size=20), axis_title=element_text(size=20), axis_text=element_text(size=16))
    + ggsize(1600, 900)
)

# Save (scale 3x to get 4800 × 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)
