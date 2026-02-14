""" pyplots.ai
bar-basic: Basic Bar Chart
Library: plotnine 0.15.3 | Python 3.14
Quality: 82/100 | Created: 2025-12-23
"""

import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_bar,
    geom_text,
    ggplot,
    labs,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"],
        "value": [45200, 32800, 28500, 19700, 15300, 12400],
    }
)
data["category"] = pd.Categorical(
    data["category"], categories=data.sort_values("value", ascending=False)["category"], ordered=True
)

# Plot
plot = (
    ggplot(data, aes(x="category", y="value"))
    + geom_bar(stat="identity", fill="#306998", width=0.7)
    + geom_text(aes(label="value"), va="bottom", size=14, format_string="${:,.0f}")
    + scale_y_continuous(labels=lambda vals: [f"${v / 1000:.0f}K" for v in vals])
    + labs(x="Product Category", y="Sales", title="bar-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=0, ha="center"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(alpha=0.2, size=0.5),
        axis_ticks=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300)
