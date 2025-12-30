""" pyplots.ai
bar-sorted: Sorted Bar Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
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
    theme,
    theme_minimal,
)


# Data - Monthly sales by product category (sorted descending)
data = {
    "category": ["Electronics", "Furniture", "Clothing", "Food & Beverage", "Home & Garden", "Sports", "Books", "Toys"],
    "sales": [4850, 3720, 3150, 2890, 2340, 1980, 1450, 920],
}
df = pd.DataFrame(data)

# Sort by sales descending and create ordered categorical for proper bar order
df = df.sort_values("sales", ascending=False)
df["category"] = pd.Categorical(df["category"], categories=df["category"], ordered=True)

# Create plot
plot = (
    ggplot(df, aes(x="category", y="sales"))
    + geom_bar(stat="identity", fill="#306998", width=0.7)
    + geom_text(aes(label="sales"), va="bottom", size=12, nudge_y=80, color="#333333")
    + labs(x="Product Category", y="Sales ($ thousands)", title="bar-sorted · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(angle=30, ha="right"),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_major_y=element_line(alpha=0.3),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
