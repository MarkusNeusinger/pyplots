"""
bar-basic: Basic Bar Chart
Library: plotnine
"""

import pandas as pd
from plotnine import aes, geom_bar, ggplot, labs, scale_y_continuous, theme, theme_minimal
from plotnine.themes.elements import element_blank, element_line


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Preserve category order
data["category"] = pd.Categorical(data["category"], categories=data["category"], ordered=True)

# Plot
plot = (
    ggplot(data, aes(x="category", y="value"))
    + geom_bar(stat="identity", fill="#306998", width=0.7)
    + labs(x="Category", y="Value", title="Basic Bar Chart")
    + scale_y_continuous(expand=(0, 0, 0.05, 0))
    + theme_minimal(base_size=16)
    + theme(
        figure_size=(16, 9),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(alpha=0.3),
    )
)

# Save
plot.save("plot.png", dpi=300)
