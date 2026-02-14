"""pyplots.ai
bar-basic: Basic Bar Chart
Library: plotnine 0.15.3 | Python 3.14
Quality: 82/100 | Created: 2025-12-23
"""

import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_bar,
    geom_text,
    ggplot,
    guides,
    labs,
    scale_fill_manual,
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

# Highlight the leading category
data["highlight"] = data["value"] == data["value"].max()

# Annotation: how far ahead is the leader
top_val = data["value"].max()
second_val = data["value"].nlargest(2).iloc[1]
lead_pct = (top_val - second_val) / second_val * 100

# Plot
plot = (
    ggplot(data, aes(x="category", y="value", fill="highlight"))
    + geom_bar(stat="identity", width=0.7)
    + scale_fill_manual(values={True: "#306998", False: "#7BA7C9"})
    + guides(fill="none")
    + geom_text(aes(label="value"), va="bottom", size=14, format_string="${:,.0f}")
    + annotate(
        "text",
        x=1,
        y=top_val + 2800,
        label=f"▲ {lead_pct:.0f}% ahead of 2nd place",
        size=12,
        color="#306998",
        fontstyle="italic",
    )
    + scale_y_continuous(
        labels=lambda vals: [f"${v / 1000:.0f}K" for v in vals], limits=(0, 52000), breaks=range(0, 55000, 10000)
    )
    + labs(x="Product Category", y="Sales (USD)", title="bar-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=0, ha="center"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(alpha=0.2, size=0.5),
        axis_ticks=element_blank(),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="white", color="white"),
    )
)

# Save
plot.save("plot.png", dpi=300)
