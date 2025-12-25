"""pyplots.ai
bar-stacked: Stacked Bar Chart
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import pandas as pd
from plotnine import (
    aes,
    element_text,
    geom_bar,
    geom_text,
    ggplot,
    labs,
    position_stack,
    scale_fill_manual,
    theme,
    theme_minimal,
)


# Data - Quarterly sales by product category
data = {
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 4,
    "Category": ["Electronics"] * 4 + ["Clothing"] * 4 + ["Home"] * 4 + ["Sports"] * 4,
    "Sales": [
        # Electronics
        45,
        52,
        48,
        68,
        # Clothing
        32,
        38,
        55,
        42,
        # Home
        28,
        31,
        35,
        38,
        # Sports
        18,
        22,
        28,
        25,
    ],
}

df = pd.DataFrame(data)

# Order categories for consistent stacking (largest at bottom)
category_order = ["Electronics", "Clothing", "Home", "Sports"]
df["Category"] = pd.Categorical(df["Category"], categories=category_order, ordered=True)

# Colors - Python Blue, Python Yellow, plus colorblind-safe additions
colors = {"Electronics": "#306998", "Clothing": "#FFD43B", "Home": "#7B68EE", "Sports": "#20B2AA"}

# Plot
plot = (
    ggplot(df, aes(x="Quarter", y="Sales", fill="Category"))
    + geom_bar(stat="identity", position="stack", width=0.7)
    + geom_text(aes(label="Sales"), position=position_stack(vjust=0.5), size=12, color="white", fontweight="bold")
    + scale_fill_manual(values=colors)
    + labs(title="bar-stacked · plotnine · pyplots.ai", x="Quarter", y="Sales (thousands USD)", fill="Product Category")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="right",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
