"""
bar-basic: Basic Bar Chart
Library: plotnine
"""

import pandas as pd
from plotnine import aes, element_text, geom_bar, geom_text, ggplot, labs, theme, theme_minimal


# Data
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"],
        "value": [45200, 32800, 28500, 19700, 15300, 12400],
    }
)

# Plot
plot = (
    ggplot(data, aes(x="category", y="value"))
    + geom_bar(stat="identity", fill="#306998", width=0.7)
    + geom_text(aes(label="value"), va="bottom", size=14, format_string="${:,.0f}")
    + labs(x="Product Category", y="Sales ($)", title="Quarterly Sales by Product Category")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=0, ha="center"),
    )
)

# Save
plot.save("plot.png", dpi=300)
